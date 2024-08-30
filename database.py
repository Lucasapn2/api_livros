from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Remova o `connect_args` porque não é necessário para bancos de dados como PostgreSQL ou MySQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
