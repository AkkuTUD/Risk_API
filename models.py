from sqlalchemy import Column, Integer, String, Enum
from database import Base
import enum

class RiskStatus(str, enum.Enum):
    new = "new"
    in_process = "in_process"
    completed = "completed"

class Risk(Base):
    __tablename__ = "risks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    status = Column(Enum(RiskStatus), default=RiskStatus.in_process)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    risk_id = Column(Integer)
    assignee = Column(String)
    status = Column(String, default="pending")