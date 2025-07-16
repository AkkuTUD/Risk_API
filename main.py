from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session
import time
from models import RiskStatus, Risk, Task
from schemas import RiskCreate, RiskOut, TaskOut
from database import SessionLocal, engine, Base
from typing import List, Optional

#Create the database
Base.metadata.create_all(engine)

#Initialize the application
app = FastAPI()

#Function to get database session
def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def process_risk(risk_id: int, db: Session):
    time.sleep(10)
    risk = db.query(Risk).filter(Risk.id == risk_id).first()
    if risk:
        risk.status = RiskStatus.completed
        db.commit()


@app.get("/")
def home():
    return "Risk API"

@app.post("/risks", response_model=RiskOut)
def create_risk(risk: RiskCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    new_risk = Risk(title=risk.title, description=risk.description, category=risk.category)
    db.add(new_risk)
    db.commit()
    db.refresh(new_risk)

    for assignee in ["security officer", "team leader"]:
        task = Task(risk_id=new_risk.id, assignee=assignee)
        db.add(task)

    db.commit()
    background_tasks.add_task(process_risk, new_risk.id, db)
    tasks = db.query(Task).filter(Task.risk_id == new_risk.id).all()

    return RiskOut(**new_risk.__dict__, tasks=tasks)

@app.get("/risks", response_model=List[RiskOut])
def get_all_risks(db: Session = Depends(get_db)):
    risks = db.query(Risk).all()
    results = []
    for r in risks:
        tasks = db.query(Task).filter(Task.risk_id == r.id).all()
        results.append(RiskOut(**r.__dict__, tasks=tasks))
    return results

@app.get("/risks/{risk_id}", response_model=RiskOut)
def get_risk(risk_id: int, db: Session = Depends(get_db)):
    risk = db.query(Risk).filter(Risk.id == risk_id).first()
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    tasks = db.query(Task).filter(Task.risk_id == risk_id).all()
    return RiskOut(**risk.__dict__, tasks=tasks)