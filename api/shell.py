# shell.py
import sys
from sqlalchemy.orm import Session
from api.database import SessionLocal, engine, Base
from api.models.local_file import LocalFile
from api.models_crud.local_file import LocalFileCrud

# Initialize database
Base.metadata.create_all(bind=engine)

# Create a new database session
db = SessionLocal()

# Make objects available in the shell
file_handler = LocalFileCrud()
