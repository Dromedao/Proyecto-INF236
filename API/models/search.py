from config.database import Base
from sqlalchemy import Column, Integer, String, Float, JSON

class Search(Base):
    __tablename__ = "searchs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prompt = Column(String)
    workshoppers = Column(JSON)
    materials = Column(JSON)