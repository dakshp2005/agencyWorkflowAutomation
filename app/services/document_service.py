import os, json, re
from datetime import datetime
from pathlib import Path
import google.generativeai as genai
from app.models.document import Document
from app.models.interaction_log import InteractionLog
from app.models.client import Client
from app.services.rag_service import rag_service
from app.services.slack_service import slack_service
from app.services.notification_service import notification_service
from app.extensions import db
from app.services.ai_utils import extract_json

OUTPUT_DIR = Path("outputs")

class DocumentService:

    def generate_proposal(self, client_id: int) -> dict:
        """Generate a full proposal document for a client using RAG + Gemini"""
        client = Client.query.get_or_404(client_id)
        
        base_prompt = f"""
You are a senior consultant writing a business proposal for a potential client.

Client Details:
- Name: {client.name}
- Company: {client.company}
- Industry: {client.industry}
- Website: {client.website or 'N/A'}
- Requirements/Preferences: {client.preferences or 'Not specified'}

Write a complete, professional proposal with these sections:
1. Executive Summary (2-3 sentences about understanding their need)
2. Understanding of Requirements (based on their industry and stated preferences)
3. Proposed Solution & Scope of Work (3-4 specific deliverables)
4. Project Timeline (realistic 4-8 week plan with phases)
5. Investment & Pricing (placeholder ranges appropriate for the industry)
6. Why Us (3 compelling differentiators)
7. Next Steps (clear CTA)

Use professional language, be specific to their industry, personalize based on context.
Format with clear section headers using markdown (## for headers).
Total length: 400-600 words.
Return ONLY the proposal content in markdown. No JSON wrapper.
"""
        enriched = rag_service.build_enriched_prompt(
            base_prompt, client_id,
            query_hint=f"proposal for {client.industry} client {client.company}"
        )
        
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(enriched)
        content = response.text.strip()
        
        title = f"Proposal for {client.company} — {datetime.now().strftime('%B %Y')}"
        
        OUTPUT_DIR.mkdir(exist_ok=True)
        (OUTPUT_DIR / "proposals").mkdir(exist_ok=True)
        filename = f"proposal_{client_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        file_path = OUTPUT_DIR / "proposals" / filename
        file_path.write_text(content, encoding='utf-8')
        
        doc = Document(
            client_id=client_id,
            title=title,
            doc_type="proposal",
            content=content,
            file_path=str(file_path),
            status="pending_approval"
        )
        db.session.add(doc)
        db.session.add(InteractionLog(
            client_id=client_id,
            action_type="document_generated",
            description=f"Proposal generated for {client.name}",
            metadata_info={"title": title}
        ))
        db.session.commit()
        
        rag_service.add_document(content, client_id, "proposal")
        
        # Create notification for document approval
        notification_service.notify_document_approval_required(doc.id, client.name, title)
        
        slack_service.notify_approval_required(
            action_type="proposal",
            action_id=doc.id,
            title=f"Proposal ready for {client.name} ({client.company})",
            preview=content[:300] + "..."
        )
        
        return {"doc_id": doc.id, "title": title, "file_path": str(file_path)}

    def generate_report(self, client_id: int, meeting_id: int = None) -> dict:
        """Generate a post-meeting summary report"""
        client = Client.query.get_or_404(client_id)
        
        base_prompt = f"""
Write a professional post-meeting summary report for {client.name} from {client.company}.

Include:
1. Meeting Summary (key points discussed based on context)
2. Client Requirements Identified
3. Agreed Next Steps
4. Action Items (with owner: Agency / Client)
5. Follow-up Timeline

Keep it concise, professional, and actionable.
Format with markdown headers.
"""
        enriched = rag_service.build_enriched_prompt(base_prompt, client_id, query_hint="meeting summary action items")
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(enriched)
        content = response.text.strip()
        
        title = f"Meeting Report — {client.company} — {datetime.now().strftime('%B %d, %Y')}"
        (OUTPUT_DIR / "reports").mkdir(parents=True, exist_ok=True)
        filename = f"report_{client_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        file_path = OUTPUT_DIR / "reports" / filename
        file_path.write_text(content, encoding='utf-8')
        
        doc = Document(client_id=client_id, title=title, doc_type="report",
                       content=content, file_path=str(file_path), status="draft")
        db.session.add(doc)
        db.session.commit()
        return {"doc_id": doc.id, "title": title}

document_service = DocumentService()
