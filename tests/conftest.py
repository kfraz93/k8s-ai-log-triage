import os

os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault(
    "POSTGRES_PORT", "5433"
)  # Using 5433 to avoid local Windows conflicts
os.environ.setdefault("POSTGRES_USER", "postgres")
os.environ.setdefault("POSTGRES_PASSWORD", "postgrespassword")
os.environ.setdefault("POSTGRES_DB", "log_triage")
os.environ.setdefault("OLLAMA_BASE_URL", "http://localhost:11434")
