from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from api.models import LocalFile

class LocalFileCrud():

    def get_local_file(self, file_id: str, db: Session):
        return db.query(LocalFile).filter(LocalFile.id == file_id).first()
    
    def create_local_file(self, db: Session, file: LocalFile):
        print("Creating file in db...")
        db.add(file)
        db.commit()
        db.refresh(file)
        return file
    
    def update_local_file(self, file_id: str, db: Session, status: str = None, path:str = None):
        file = db.query(LocalFile).filter(LocalFile.id == file_id).first()
        if status:
            file.status = status
        if path:
            file.path = path
        try:
            db.commit()
            db.refresh(file)
            return file
        except IntegrityError as e:
            db.rollback()
            raise e
        

