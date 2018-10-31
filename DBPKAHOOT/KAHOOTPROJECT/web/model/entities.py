from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import connector


class User(connector.Manager.Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    nickname = Column(String(12))

class Sala(connector.Manager.Base):
    __tablename__ = 'salones'
    id = Column(Integer, Sequence('sala_id_seq'), primary_key=True)
    pin = Column(String(10))
    name = Column(String(20))


class Message(connector.Manager.Base):
    __tablename__ = 'messages'
    id = Column(Integer, Sequence('message_id_seq'), primary_key=True)
    content = Column(String(500))
    sala_to_id = Column(Integer, ForeignKey('salones.id'))
    sala_to = relationship(Sala, foreign_keys=[sala_to_id])


class Contador(connector.Manager.Base):
    __tablename__ = 'contador'
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
