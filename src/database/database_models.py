from sqlalchemy import String, Integer, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database.database_connection import Base, engine


class DBLead(Base):
    __tablename__ = "lead"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(3))
    samples = Column(Integer, default=None)
    ecg_id = Column(ForeignKey("ecg.id"))
    signal = Column(String(256), default=0)


class DBEcg(Base):
    __tablename__ = "ecg"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    user_id = Column(ForeignKey("user.id"))
    leads = relationship(DBLead)


class DBUser(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256))
    password = Column(String(60))
    is_admin = Column(Integer, default=0)
    ecgs = relationship(DBEcg)


Base.metadata.create_all(engine)
