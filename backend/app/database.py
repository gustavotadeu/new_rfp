import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

connect_args = {}
engine_options = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    if DATABASE_URL == "sqlite:///:memory:":
        engine_options["poolclass"] = StaticPool

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    **engine_options,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
