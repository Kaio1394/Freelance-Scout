from app.db.database import Base
from sqlalchemy import Column, String
import uuid

class Freelancer(Base):
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)