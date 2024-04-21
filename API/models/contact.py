from config.database import Base
from sqlalchemy import Column, Integer, String, Float, JSON

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    state = Column(Integer) #0 Esperando 1 Respondido 2 Sin respuesta
    decision = Column(Integer) #0 Sin desición 1 Aceptado 2 Rechazado