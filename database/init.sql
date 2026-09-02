-- Enable the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table for storing historical incident logs and embeddings
CREATE TABLE IF NOT EXISTS incident_logs (
    id SERIAL PRIMARY KEY,
    error_message TEXT NOT NULL,
    service_name VARCHAR(100) NOT NULL,
    root_cause TEXT NOT NULL,
    remediation TEXT NOT NULL,
    embedding vector(768),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create an HNSW index for fast cosine similarity searches
CREATE INDEX IF NOT EXISTS incident_logs_embedding_hnsw_idx
ON incident_logs
USING hnsw (embedding vector_cosine_ops);
