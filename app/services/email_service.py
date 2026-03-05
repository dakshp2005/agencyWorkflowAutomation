import smtplib, imaplib, email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai
from app.services.rag_service import rag_service
from app.services.slack_service import slack_service
from app.models.email_record import EmailRecord
from app.models.client import Client
from app.models.interaction_log import InteractionLog
from app.extensions import db
from app.config import Config
from app.services.ai_utils import extract_json
from datetime import datetime

class EmailService:

    def generate_outreach_email(self, client_id: int, email_type: str = "outreach") -> dict:
        """
        Generate a personalized email using Gemini + RAG context.
        Saves as 'pending_approval'. Does NOT send.
        Returns: {email_id, subject, body}
        """
        client = Client.query.get_or_404(client_id)
        
        base_prompt = f"""
You are writing a professional outreach email for a marketing/consulting agency.

Client Information:
- Name: {client.name}
- Company: {client.company}
- Industry: {client.industry}
- Website: {client.website or 'N/A'}
- Known Preferences/Requirements: {client.preferences or 'Not specified'}
- Internal Notes: {client.notes or 'None'}

Write a {email_type} email that:
1. Addresses the client by first name
2. References their industry and specific business context
3. Presents the agency's value proposition relevant to their needs
4. Has a clear, soft call-to-action (schedule a call, reply with questions)
5. Sounds human, warm, and professional — NOT like a template
6. Is concise (150-200 words max for the body)

Return ONLY a JSON object with this exact structure:
{{"subject": "...", "body": "..."}}
No extra text, no markdown, just the JSON.
"""
        enriched_prompt = rag_service.build_enriched_prompt(
            base_prompt, client_id, 
            query_hint=f"outreach email for {client.industry} agency client"
        )
        
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(enriched_prompt)
        
        try:
            data = extract_json(response.text)
            if not data or "subject" not in data or "body" not in data:
                raise ValueError("AI returned invalid JSON structure")
        except Exception as e:
            print(f"[EmailService] Error parsing AI response: {e}")
            # Fallback for when AI fails or returns garbage
            data = {
                "subject": f"Automated Outreach: {client.company}",
                "body": f"Hi {client.name},\n\nI'm reaching out from our agency regarding your work in {client.industry}."
            }
        
        record = EmailRecord(
            client_id=client_id,
            subject=data["subject"],
            body=data["body"],
            email_type=email_type,
            status="pending_approval"
        )
        db.session.add(record)
        
        log = InteractionLog(
            client_id=client_id,
            action_type="email_generated",
            description=f"{email_type.title()} email generated for {client.name}",
            metadata_info={"email_id": None, "type": email_type}
        )
        db.session.add(log)
        db.session.commit()
        
        log.metadata_info = {"email_id": record.id, "type": email_type}
        db.session.commit()
        
        # Add generated email to RAG for future context
        rag_service.add_document(f"Subject: {data['subject']}\n{data['body']}", client_id, "email")
        
        # Notify operator via Slack
        slack_service.notify_approval_required(
            action_type="email",
            action_id=record.id,
            title=f"New {email_type} email ready for {client.name}",
            preview=data["body"][:200] + "..."
        )
        
        return {"email_id": record.id, "subject": data["subject"], "body": data["body"]}

    def send_email(self, email_id: int) -> bool:
        """Send an approved email via Gmail SMTP"""
        record = EmailRecord.query.get_or_404(email_id)
        client = Client.query.get(record.client_id)
        
        try:
            msg = MIMEMultipart()
            msg['From'] = Config.GMAIL_USER
            msg['To'] = client.email
            msg['Subject'] = record.subject
            msg.attach(MIMEText(record.body, 'plain'))
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(Config.GMAIL_USER, Config.GMAIL_APP_PASSWORD)
                server.send_message(msg)
            
            record.status = 'sent'
            record.sent_at = datetime.utcnow()
            client.status = 'outreach_sent'
            
            db.session.add(InteractionLog(
                client_id=record.client_id,
                action_type="email_sent",
                description=f"Email sent to {client.email}",
                metadata_info={"email_id": email_id}
            ))
            db.session.commit()
            return True
            
        except Exception as e:
            record.status = 'failed'
            db.session.commit()
            raise e

    def approve_and_send(self, email_id: int) -> bool:
        """Mark email as approved and send immediately"""
        record = EmailRecord.query.get_or_404(email_id)
        record.status = 'approved'
        db.session.commit()
        return self.send_email(email_id)

    def reject_email(self, email_id: int) -> None:
        """Reject an email draft"""
        record = EmailRecord.query.get_or_404(email_id)
        record.status = 'draft'
        db.session.commit()

email_service = EmailService()
