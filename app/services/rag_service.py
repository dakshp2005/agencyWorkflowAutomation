import os, json, pickle
from pathlib import Path
import faiss
import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter
import google.generativeai as genai
from app.models.rag_document import RAGDocument
from app.models.interaction_log import InteractionLog
from app.extensions import db

FAISS_INDEX_PATH = Path("data/faiss_index")
EMBEDDING_DIM = 3072   # Gemini gemini-embedding-001 output dimension

class RAGService:

    def __init__(self):
        self.index = None
        self.metadata_store = []    # List of dicts: {client_id, source_type, text_chunk, db_id}
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        self._load_or_create_index()

    def _load_or_create_index(self):
        FAISS_INDEX_PATH.mkdir(parents=True, exist_ok=True)
        index_file = FAISS_INDEX_PATH / "index.faiss"
        meta_file = FAISS_INDEX_PATH / "metadata.pkl"
        if index_file.exists() and meta_file.exists():
            self.index = faiss.read_index(str(index_file))
            with open(meta_file, "rb") as f:
                self.metadata_store = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(EMBEDDING_DIM)
            self.metadata_store = []

    def _save_index(self):
        faiss.write_index(self.index, str(FAISS_INDEX_PATH / "index.faiss"))
        with open(FAISS_INDEX_PATH / "metadata.pkl", "wb") as f:
            pickle.dump(self.metadata_store, f)

    def _get_embedding(self, text: str) -> np.ndarray:
        result = genai.embed_content(
            model="models/gemini-embedding-001",
            content=text,
            task_type="retrieval_document"
        )
        return np.array(result['embedding'], dtype=np.float32)

    def _get_query_embedding(self, text: str) -> np.ndarray:
        result = genai.embed_content(
            model="models/gemini-embedding-001",
            content=text,
            task_type="retrieval_query"
        )
        return np.array(result['embedding'], dtype=np.float32)

    def add_document(self, text: str, client_id: int, source_type: str) -> int:
        """Chunk text, embed, add to FAISS, save to DB. Returns RAGDocument.id"""
        chunks = self.splitter.split_text(text)
        if not chunks:
            return None
        embeddings = []
        faiss_ids = []
        start_id = self.index.ntotal
        for i, chunk in enumerate(chunks):
            emb = self._get_embedding(chunk)
            embeddings.append(emb)
            faiss_ids.append(start_id + i)
            self.metadata_store.append({
                "client_id": client_id,
                "source_type": source_type,
                "text": chunk,
                "faiss_id": start_id + i
            })
        matrix = np.stack(embeddings)
        self.index.add(matrix)
        self._save_index()
        rag_doc = RAGDocument(
            client_id=client_id,
            source_type=source_type,
            raw_text=text,
            chunk_count=len(chunks),
            faiss_ids=faiss_ids
        )
        db.session.add(rag_doc)
        db.session.commit()
        return rag_doc.id

    def retrieve_context(self, query: str, client_id: int = None, top_k: int = 5) -> str:
        """Search FAISS index, optionally filter by client_id, return context string"""
        if self.index.ntotal == 0:
            return ""
        query_emb = self._get_query_embedding(query)
        query_matrix = np.array([query_emb])
        k = min(top_k * 3, self.index.ntotal)  # Fetch extra to allow filtering
        distances, indices = self.index.search(query_matrix, k)
        results = []
        for idx in indices[0]:
            if idx < 0 or idx >= len(self.metadata_store):
                continue
            meta = self.metadata_store[idx]
            if client_id is not None and meta.get("client_id") != client_id:
                continue
            results.append(meta["text"])
            if len(results) >= top_k:
                break
        return "\n\n---\n\n".join(results)

    def build_enriched_prompt(self, base_prompt: str, client_id: int, query_hint: str = "") -> str:
        """Retrieve relevant context and prepend to prompt"""
        context = self.retrieve_context(query_hint or base_prompt, client_id=client_id)
        if context:
            return f'''RELEVANT CONTEXT FROM PAST CLIENT INTERACTIONS:
{context}

---

TASK:
{base_prompt}'''
        return base_prompt

    def index_all_existing_data(self):
        """Bootstrap: index all existing DB records into FAISS"""
        from app.models.email_record import EmailRecord
        from app.models.reply import InboundReply
        from app.models.document import Document
        from app.models.client import Client

        for client in Client.query.all():
            text = f"Client: {client.name}, Company: {client.company}, Industry: {client.industry}, Preferences: {client.preferences}, Notes: {client.notes}"
            self.add_document(text, client.id, "registration")
        for email in EmailRecord.query.filter_by(status='sent').all():
            self.add_document(f"Subject: {email.subject}\n{email.body}", email.client_id, "email")
        for reply in InboundReply.query.all():
            self.add_document(reply.raw_body, reply.client_id, "reply")
        for doc in Document.query.all():
            self.add_document(doc.content, doc.client_id, "proposal")

rag_service = RAGService()
