import os, json
from app.services.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as genai
from app.models.rag_document import RAGDocument
from app.models.interaction_log import InteractionLog
from app.extensions import db
from sqlalchemy import text

EMBEDDING_DIM = 3072

class RAGService:

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    def _get_embedding(self, text: str) -> list:
        result = genai.embed_content(
            model="models/gemini-embedding-001",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']

    def _get_query_embedding(self, text: str) -> list:
        result = genai.embed_content(
            model="models/gemini-embedding-001",
            content=text,
            task_type="retrieval_query"
        )
        return result['embedding']

    def add_document(self, text: str, client_id: int, source_type: str) -> int:
        chunks = self.splitter.split_text(text)
        if not chunks:
            return None

        rag_doc = RAGDocument(
            client_id=client_id,
            source_type=source_type,
            raw_text=text,
            chunk_count=len(chunks),
            faiss_ids=[]
        )
        db.session.add(rag_doc)
        db.session.flush()

        for i, chunk in enumerate(chunks):
            emb = self._get_embedding(chunk)
            embedding_str = '[' + ','.join(str(x) for x in emb) + ']'
            db.session.execute(
                text("""
                    INSERT INTO rag_chunks (rag_document_id, client_id, chunk_text, chunk_index, embedding)
                    VALUES (:rag_doc_id, :client_id, :chunk_text, :chunk_index, :embedding::vector)
                """),
                {
                    "rag_doc_id": rag_doc.id,
                    "client_id": client_id,
                    "chunk_text": chunk,
                    "chunk_index": i,
                    "embedding": embedding_str
                }
            )

        db.session.commit()
        return rag_doc.id

    def retrieve_context(self, query: str, client_id: int = None, top_k: int = 5) -> str:
        query_emb = self._get_query_embedding(query)
        embedding_str = '[' + ','.join(str(x) for x in query_emb) + ']'

        if client_id is not None:
            results = db.session.execute(
                text("""
                    SELECT chunk_text, 1 - (embedding <=> :query::vector) AS similarity
                    FROM rag_chunks
                    WHERE client_id = :client_id
                    ORDER BY embedding <=> :query::vector
                    LIMIT :limit
                """),
                {"query": embedding_str, "client_id": client_id, "limit": top_k}
            ).fetchall()
        else:
            results = db.session.execute(
                text("""
                    SELECT chunk_text, 1 - (embedding <=> :query::vector) AS similarity
                    FROM rag_chunks
                    ORDER BY embedding <=> :query::vector
                    LIMIT :limit
                """),
                {"query": embedding_str, "limit": top_k}
            ).fetchall()

        if not results:
            return ""
        return "\n\n---\n\n".join([r[0] for r in results])

    def build_enriched_prompt(self, base_prompt: str, client_id: int, query_hint: str = "") -> str:
        context = self.retrieve_context(query_hint or base_prompt, client_id=client_id)
        if context:
            return f'''RELEVANT CONTEXT FROM PAST CLIENT INTERACTIONS:
{context}

---

TASK:
{base_prompt}'''
        return base_prompt

    def index_all_existing_data(self):
        from app.models.email_record import EmailRecord
        from app.models.reply import InboundReply
        from app.models.document import Document
        from app.models.client import Client

        for client in Client.query.all():
            text_content = f"Client: {client.name}, Company: {client.company}, Industry: {client.industry}, Preferences: {client.preferences}, Notes: {client.notes}"
            self.add_document(text_content, client.id, "registration")
        for email in EmailRecord.query.filter_by(status='sent').all():
            self.add_document(f"Subject: {email.subject}\n{email.body}", email.client_id, "email")
        for reply in InboundReply.query.all():
            self.add_document(reply.raw_body, reply.client_id, "reply")
        for doc in Document.query.all():
            self.add_document(doc.content, doc.client_id, "proposal")

rag_service = RAGService()
