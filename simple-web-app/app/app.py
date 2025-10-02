from fastapi import FastAPI, Form, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Submission

app = FastAPI()
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)  # Create tables on startup

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_submissions(request: Request, db: Session = Depends(get_db)):
    submissions = db.query(Submission).order_by(Submission.created_at.desc()).limit(5).all()
    return templates.TemplateResponse("index.html", {"request": request, "submissions": submissions})

@app.post("/submit/")
def submit_text(text: str = Form(...), db: Session = Depends(get_db)):
    new_submission = Submission(text=text)
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return {"message": "Submission added"}