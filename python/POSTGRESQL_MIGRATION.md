# PostgreSQL Migration Guide

This document outlines considerations for migrating from SQLite to PostgreSQL.

## Current Setup (SQLite Compatible)

The codebase is designed to be PostgreSQL-ready with minor adjustments:

### ✅ Already Compatible

1. **SQLModel/SQLAlchemy** - Works with both databases
2. **Alembic migrations** - Will work with PostgreSQL
3. **JSON fields** - Currently stored as TEXT with json.loads/dumps (works everywhere)
4. **Foreign keys** - Supported by both
5. **Data types** - Using SQLAlchemy types (Integer, String, Boolean, DateTime) which map correctly

### ⚠️ Minor Issues Fixed

1. **Boolean server_default** - Changed from `'0'` to `sa.false()` for PostgreSQL compatibility
2. **Database URL** - Made configurable via `DATABASE_URL` environment variable

## When Ready to Migrate to PostgreSQL

### 1. Update Database URL

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/partytime"
```

Or update `database.py` directly:
```python
database_url = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/dbname")
```

### 2. Install PostgreSQL Driver

Add to `requirements.txt`:
```
psycopg2-binary
```

### 3. Create PostgreSQL Database

```sql
CREATE DATABASE partytime;
```

### 4. Run Migrations

```bash
alembic upgrade head
```

The existing migrations should work as-is since we're using SQLAlchemy types.

### 5. (Optional) Migrate JSON Fields to PostgreSQL JSONB

PostgreSQL has native JSONB support which is more efficient than TEXT + json.loads:

```python
# In models.py, change:
attendee_ids: str = Field(default="[]")

# To:
attendee_ids: dict = Field(default={}, sa_column=Column(JSON))

# Then update helper functions to work with dict directly
```

**Note:** This requires a migration. Current TEXT approach works fine and is more portable.

### 6. Consider PostGIS for Location Queries

You already have `latitude` and `longitude` fields. PostgreSQL with PostGIS extension can do efficient spatial queries:

```python
# Install: CREATE EXTENSION postgis;
# Then use PostGIS geometry types for better performance
```

### 7. Update Connection Pool Settings

PostgreSQL benefits from connection pooling:

```python
engine = create_engine(
    database_url,
    pool_size=10,
    max_overflow=20
)
```

## Current Status

- ✅ All migrations are PostgreSQL-compatible
- ✅ Boolean defaults fixed
- ✅ Database URL is configurable
- ✅ SQLModel/SQLAlchemy abstractions handle differences
- ⚠️ JSON fields are TEXT-based (works but could be optimized later)
- ⚠️ No PostGIS integration yet (optional optimization)

## Testing PostgreSQL Locally

```bash
# Install PostgreSQL client libraries
pip install psycopg2-binary

# Set DATABASE_URL
export DATABASE_URL="postgresql://localhost/partytime"

# Run migrations
alembic upgrade head

# Start your app
uvicorn main:app --reload
```

Your codebase should work with PostgreSQL with minimal changes!

