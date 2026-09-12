-- =============================================
-- AGENCY WORKFLOW AUTOMATION - SUPABASE SCHEMA
-- =============================================

-- Enable pgvector extension for vector search
CREATE EXTENSION IF NOT EXISTS vector;

-- Drop old tables from previous schema version
DROP TABLE IF EXISTS interactions CASCADE;
DROP TABLE IF EXISTS approvals CASCADE;
DROP TABLE IF EXISTS campaigns CASCADE;
DROP TABLE IF EXISTS clients CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- =============================================
-- 1. USER TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) UNIQUE,
    email VARCHAR(120) UNIQUE,
    password_hash VARCHAR(256),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_user_username ON "user"(username);
CREATE INDEX IF NOT EXISTS ix_user_email ON "user"(email);

-- =============================================
-- 2. CLIENT TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS client (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE,
    company VARCHAR(120),
    industry VARCHAR(80),
    website VARCHAR(200),
    phone VARCHAR(30),
    preferences TEXT,
    notes TEXT,
    status VARCHAR(30) DEFAULT 'new',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- =============================================
-- 3. LEAD TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS lead (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    company VARCHAR(100),
    website VARCHAR(200),
    email VARCHAR(120),
    industry VARCHAR(100),
    domain_topic VARCHAR(100),
    description TEXT,
    icp_score INTEGER DEFAULT 0,
    icp_reasoning TEXT,
    status VARCHAR(20) DEFAULT 'new',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- =============================================
-- 4. EMAIL_RECORD TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS email_record (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES client(id) ON DELETE CASCADE,
    subject VARCHAR(300),
    body TEXT,
    email_type VARCHAR(30) DEFAULT 'outreach',
    status VARCHAR(20) DEFAULT 'draft',
    approved_by VARCHAR(80),
    sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =============================================
-- 5. INBOUND_REPLY TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS inbound_reply (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES client(id) ON DELETE SET NULL,
    sender_email VARCHAR(120),
    subject VARCHAR(300),
    raw_body TEXT,
    classification VARCHAR(20),
    extracted_entities JSONB,
    action_taken VARCHAR(100),
    processed_at TIMESTAMP DEFAULT NOW()
);

-- =============================================
-- 6. MEETING TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS meeting (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES client(id) ON DELETE CASCADE,
    proposed_slots JSONB,
    confirmed_slot VARCHAR(50),
    calendar_event_id VARCHAR(200),
    meeting_link VARCHAR(300),
    agenda TEXT,
    status VARCHAR(20) DEFAULT 'proposed',
    created_at TIMESTAMP DEFAULT NOW()
);

-- =============================================
-- 7. DOCUMENT TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS document (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES client(id) ON DELETE CASCADE,
    title VARCHAR(200),
    doc_type VARCHAR(30),
    content TEXT,
    file_path VARCHAR(300),
    status VARCHAR(20) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT NOW()
);

-- =============================================
-- 8. RAG_DOCUMENT TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS rag_document (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES client(id) ON DELETE SET NULL,
    source_type VARCHAR(30),
    raw_text TEXT,
    chunk_count INTEGER DEFAULT 0,
    faiss_ids JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =============================================
-- 9. INTERACTION_LOG TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS interaction_log (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES client(id) ON DELETE SET NULL,
    action_type VARCHAR(50),
    description TEXT,
    metadata_info JSONB,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- =============================================
-- 10. NOTIFICATION TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS notification (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    message TEXT,
    notification_type VARCHAR(50),
    related_id INTEGER,
    related_type VARCHAR(50),
    is_read BOOLEAN DEFAULT FALSE,
    action_url VARCHAR(300),
    created_at TIMESTAMP DEFAULT NOW()
);

-- =============================================
-- 11. RAG_CHUNKS TABLE (pgvector embeddings)
-- =============================================
CREATE TABLE IF NOT EXISTS rag_chunks (
    id SERIAL PRIMARY KEY,
    rag_document_id INTEGER REFERENCES rag_document(id) ON DELETE CASCADE,
    client_id INTEGER REFERENCES client(id) ON DELETE SET NULL,
    chunk_text TEXT NOT NULL,
    chunk_index INTEGER DEFAULT 0,
    embedding vector(3072),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create vector similarity index for fast search
CREATE INDEX IF NOT EXISTS idx_rag_chunks_embedding 
    ON rag_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

CREATE INDEX IF NOT EXISTS idx_rag_chunks_client_id ON rag_chunks(client_id);

-- =============================================
-- TRIGGER: Auto-update updated_at on client
-- =============================================
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_client_modtime
    BEFORE UPDATE ON client
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_lead_modtime
    BEFORE UPDATE ON lead
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();
