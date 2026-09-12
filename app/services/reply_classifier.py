import imaplib, email as email_lib, json, re
from email.header import decode_header
import google.generativeai as genai
from app.models.reply import InboundReply
from app.models.client import Client
from app.models.interaction_log import InteractionLog
from app.services.rag_service import rag_service
from app.services.slack_service import slack_service
from app.extensions import db
from app.services.ai_utils import extract_json
from app.config import Config
from datetime import datetime

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None

class ReplyClassifier:

    def fetch_and_classify(self) -> list:
        """
        Connect to Gmail IMAP, fetch unread emails, classify each one.
        Returns list of classified reply dicts.
        """
        results = []
        try:
            mail = imaplib.IMAP4_SSL(Config.IMAP_SERVER)
            mail.login(Config.GMAIL_USER, Config.GMAIL_APP_PASSWORD)
            mail.select("inbox")
            _, message_ids = mail.search(None, 'UNSEEN')
            
            for msg_id in message_ids[0].split():
                _, data = mail.fetch(msg_id, '(RFC822)')
                raw = data[0][1]
                msg = email_lib.message_from_bytes(raw)
                
                sender = msg.get("From", "")
                sender_email = re.findall(r'[\w\.-]+@[\w\.-]+', sender)
                sender_email = sender_email[0] if sender_email else ""
                subject_raw = msg.get("Subject", "")
                subject, enc = decode_header(subject_raw)[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(enc or "utf-8")
                
                body = self._extract_body(msg)
                if not body.strip():
                    continue
                
                # Match sender to client
                client = Client.query.filter_by(email=sender_email).first()
                client_id = client.id if client else None
                
                classification_result = self._classify(body)
                
                reply = InboundReply(
                    client_id=client_id,
                    sender_email=sender_email,
                    subject=subject,
                    raw_body=body,
                    classification=classification_result["classification"],
                    extracted_entities=classification_result["entities"],
                    action_taken="pending"
                )
                db.session.add(reply)
                db.session.flush()
                
                # Index reply into RAG
                rag_service.add_document(body, client_id, "reply")
                
                # Trigger next actions
                action = self._trigger_action(reply, client)
                reply.action_taken = action
                
                db.session.add(InteractionLog(
                    client_id=client_id,
                    action_type="reply_classified",
                    description=f"Reply from {sender_email} classified as {classification_result['classification']}",
                    metadata_info={"reply_id": reply.id, "action": action}
                ))
                db.session.commit()
                results.append({"reply_id": reply.id, "classification": classification_result["classification"]})
            
            mail.logout()
        except Exception as e:
            print(f"[ReplyClassifier] Error: {e}")
        
        return results

    def _extract_body(self, msg) -> str:
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        return part.get_payload(decode=True).decode("utf-8", errors="replace")
                    except:
                        pass
        else:
            try:
                return msg.get_payload(decode=True).decode("utf-8", errors="replace")
            except:
                return ""
        return ""

    def _preprocess(self, text: str) -> str:
        if nlp:
            doc = nlp(text[:5000])
            tokens = [t.lemma_ for t in doc if not t.is_stop and not t.is_punct and t.is_alpha]
            return " ".join(tokens)
        return text

    def _classify(self, body: str) -> dict:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"""
Analyze this email reply and return ONLY a JSON object with no extra text:

Email:
\"\"\"{body[:2000]}\"\"\"

Return this exact JSON structure:
{{
  "classification": "POSITIVE" or "NEGATIVE" or "NEUTRAL",
  "intent": "BOOKING_REQUEST" or "PRICE_OBJECTION" or "TECH_QUESTION" or "UNSUBSCRIBE" or "GENERAL_INQUIRY",
  "confidence": 0.0 to 1.0,
  "sentiment_score": -1.0 to 1.0,
  "suggested_rebuttal": "One sentence suggesting how to handle this lead",
  "entities": {{
    "dates": [],
    "companies": [],
    "requirements": []
  }}
}}

INTENTS:
- BOOKING_REQUEST: Wants to meet, schedule a call, or talk.
- PRICE_OBJECTION: Complaining about cost, budget, or asking for discount.
- TECH_QUESTION: Asking about specifics, features, or how it works.
- UNSUBSCRIBE: Don't contact again, wrong person.
- GENERAL_INQUIRY: Other questions or generic replies.
"""
        try:
            response = model.generate_content(prompt)
            data = extract_json(response.text)
            if not data or "classification" not in data:
                raise ValueError("Invalid classification output")
            data["classification"] = data["classification"].upper()
            return data
        except Exception as e:
            print(f"[ReplyClassifier] Parsing Error: {e}")
            return {
                "classification": "NEUTRAL",
                "intent": "GENERAL_INQUIRY",
                "confidence": 0.5,
                "sentiment_score": 0.0,
                "suggested_rebuttal": "Awaiting manual review.",
                "entities": {"dates": [], "companies": [], "requirements": []}
            }

    def _trigger_action(self, reply: InboundReply, client: Client) -> str:
        from app.services.scheduler_service import scheduler_service
        from app.services.email_service import email_service
        
        classification = reply.classification
        
        if classification == "POSITIVE":
            if client:
                client.status = "replied"
                db.session.commit()
                scheduler_service.propose_meeting(client.id, reply.extracted_entities or {})
                slack_service.send_notification(
                    f"🟢 *Positive reply* from *{client.name}* ({reply.sender_email})\n"
                    f"Meeting slots have been proposed. Awaiting your confirmation."
                )
            return "meeting_proposed"
        
        elif classification == "NEUTRAL":
            if client:
                email_service.generate_outreach_email(client.id, email_type="followup")
                slack_service.send_notification(
                    f"🟡 *Neutral reply* from *{client.name or reply.sender_email}*\n"
                    f"Follow-up email draft created. Please review and approve."
                )
            return "followup_generated"
        
        elif classification == "NEGATIVE":
            if client:
                client.status = "not_interested"
                db.session.commit()
            slack_service.send_notification(
                f"🔴 *Negative reply* from *{client.name if client else reply.sender_email}*\n"
                f"Client marked as not interested."
            )
            return "marked_not_interested"
        
        return "logged"

reply_classifier = ReplyClassifier()
