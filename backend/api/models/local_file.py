from sqlalchemy import Column, Integer, String, Boolean
from api.database import Base


class LocalFile(Base):
    __tablename__ = "local_file"

    id = Column(String, primary_key=True, index=True)
    status = Column(String, index=True)
    path = Column(String, unique=True, index=True)
    deletion_queued = Column(Boolean, default=False)