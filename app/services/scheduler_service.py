import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from app.models.meeting import Meeting
from app.models.interaction_log import InteractionLog
from app.services.slack_service import slack_service
from app.extensions import db
from app.config import Config
import os, base64

SCOPES = ['https://www.googleapis.com/auth/calendar']

class SchedulerService:

    def _get_calendar_service(self):
        creds = None
        token_data = os.environ.get('GOOGLE_CALENDAR_TOKEN')
        
        if token_data:
            try:
                token_json = json.loads(base64.b64decode(token_data).decode())
                creds = Credentials.from_authorized_user_info(token_json, SCOPES)
            except Exception:
                pass
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception:
                    return None
            else:
                return None
        
        return build('calendar', 'v3', credentials=creds)

    def get_free_slots(self, days_ahead: int = 7) -> list:
        try:
            service = self._get_calendar_service()
            if not service:
                raise ValueError("Calendar service not available")
            
            now = datetime.utcnow()
            time_min = now.isoformat() + 'Z'
            time_max = (now + timedelta(days=days_ahead)).isoformat() + 'Z'
            
            events_result = service.events().list(
                calendarId='primary',
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            busy_times = []
            for event in events_result.get('items', []):
                start = event['start'].get('dateTime')
                end = event['end'].get('dateTime')
                if start and end:
                    busy_times.append((
                        datetime.fromisoformat(start.replace('Z', '+00:00')),
                        datetime.fromisoformat(end.replace('Z', '+00:00'))
                    ))
            
            free_slots = []
            current = now.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
            
            for _ in range(days_ahead):
                for hour in range(9, 18):
                    slot_start = current.replace(hour=hour)
                    slot_end = slot_start + timedelta(hours=1)
                    if slot_start <= now:
                        continue
                    conflict = any(
                        not (slot_end <= b[0] or slot_start >= b[1])
                        for b in busy_times
                    )
                    if not conflict:
                        free_slots.append(slot_start.isoformat())
                        if len(free_slots) >= 3:
                            return free_slots
                current += timedelta(days=1)
            
            return free_slots
            
        except Exception as e:
            print(f"[Scheduler] Calendar error: {e}. Using default slots.")
            base = datetime.utcnow() + timedelta(days=2)
            return [
                base.replace(hour=10, minute=0).isoformat(),
                base.replace(hour=14, minute=0).isoformat(),
                (base + timedelta(days=1)).replace(hour=11, minute=0).isoformat()
            ]

    def propose_meeting(self, client_id: int, entities: dict = {}) -> int:
        from app.models.client import Client
        client = Client.query.get(client_id)
        slots = self.get_free_slots()
        
        meeting = Meeting(
            client_id=client_id,
            proposed_slots=slots,
            status="proposed",
            agenda=f"Discovery call with {client.name} from {client.company}"
        )
        db.session.add(meeting)
        db.session.add(InteractionLog(
            client_id=client_id,
            action_type="meeting_proposed",
            description=f"3 meeting slots proposed for {client.name}",
            metadata_info={"slots": slots}
        ))
        db.session.commit()
        
        slot_display = "\n".join([f"• {s}" for s in slots])
        slack_service.notify_approval_required(
            action_type="meeting",
            action_id=meeting.id,
            title=f"Meeting proposed with {client.name} ({client.company})",
            preview=f"Proposed slots:\n{slot_display}"
        )
        return meeting.id

    def confirm_meeting(self, meeting_id: int, chosen_slot: str) -> dict:
        from app.models.client import Client
        meeting = Meeting.query.get_or_404(meeting_id)
        client = Client.query.get(meeting.client_id)
        
        try:
            service = self._get_calendar_service()
            if service:
                start_dt = datetime.fromisoformat(chosen_slot)
                end_dt = start_dt + timedelta(hours=1)
                
                event = {
                    'summary': f'Meeting: {client.name} - {client.company}',
                    'description': meeting.agenda,
                    'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'UTC'},
                    'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'UTC'},
                    'attendees': [{'email': client.email}],
                    'reminders': {'useDefault': True}
                }
                created = service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()
                meeting.calendar_event_id = created['id']
                meeting.meeting_link = created.get('htmlLink', '')
        except Exception as e:
            print(f"[Scheduler] Could not create calendar event: {e}")
        
        meeting.confirmed_slot = chosen_slot
        meeting.status = "confirmed"
        client.status = "meeting_scheduled"
        
        db.session.add(InteractionLog(
            client_id=meeting.client_id,
            action_type="meeting_confirmed",
            description=f"Meeting confirmed for {chosen_slot}",
            metadata_info={"meeting_id": meeting_id}
        ))
        db.session.commit()
        
        from app.services.document_service import document_service
        document_service.generate_proposal(meeting.client_id)
        
        return {"meeting_id": meeting_id, "slot": chosen_slot, "link": meeting.meeting_link}

scheduler_service = SchedulerService()
