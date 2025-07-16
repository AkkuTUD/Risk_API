from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from enum import Enum

class RiskCreate(BaseModel):
    title: str
    description: str
    category: str

class TaskOut(BaseModel):
    id: int
    assignee: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class RiskOut(BaseModel):
    id: int
    title: str
    description: str
    category: str
    status: str
    tasks: List[TaskOut] = []

    model_config = ConfigDict(from_attributes=True)