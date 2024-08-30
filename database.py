from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os

# Substitua pela URL apropriada
SQLALCHEMY_DATABASE_URL = "postgresql://bdapp_n8co_user:0MwMppnz7IwL7QtMUD5mj4ov01oKyrDV@dpg-cr8uooi3esus73bdjiig-a.oregon-postgres.render.com/bdapp_n8co"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
