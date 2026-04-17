import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load .env locally (Vercel ignores this)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./profiles.db")

# --- Fix Postgres URL if needed ---
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# --- Engine config ---
engine_args = {
    "pool_pre_ping": True,  # REQUIRED for serverless Postgres
}

if DATABASE_URL.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_args)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()


# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from dotenv import load_dotenv

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./profiles.db")  # PostgreSQL in prod

# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

# )

# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
# Base = declarative_base()