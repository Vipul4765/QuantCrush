import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Read and fix database URL
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError("DATABASE_URL not found in environment variables")

# ✅ Heroku-style URL fix (optional)
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# ✅ Create engine with pooling
engine = create_engine(
    db_url,
    pool_size=20,
    max_overflow=5,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True
)

# ✅ Create SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        print("DB Error:", str(e))  # Optional: log or raise
        raise
    finally:
        db.close()
