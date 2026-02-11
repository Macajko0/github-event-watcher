from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True)
    type = Column(String, index=True)
    created_at = Column(DateTime, index=True)

    repo_id = Column(String, ForeignKey("repos.id"))
    repo = relationship("Repo", back_populates="events")

class Repo(Base):
    __tablename__ = "repos"

    id = Column(String, primary_key=True)
    name = Column(String, index=True)
    url = Column(String, index=True)

    events = relationship("Event", back_populates="repo")