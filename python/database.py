from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager
import os

# Database URL - defaults to SQLite, can be overridden with DATABASE_URL env var
# For PostgreSQL: DATABASE_URL="postgresql://user:pass@localhost/dbname"
database_url = os.getenv("DATABASE_URL", "sqlite:///database.db")

# Create the engine once and share it
# For PostgreSQL, connect_args is empty (SQLite uses check_same_thread=False internally)
connect_args = {} if database_url.startswith("postgresql") else {}
engine = create_engine(database_url, connect_args=connect_args)

def get_db_session():
    # Create a new session for each call
    return Session(engine)