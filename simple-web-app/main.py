from fastapi import FastAPI, Form, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Submission
from prometheus_fastapi_instrumentator import Instrumentator  # Import the instrumentator
from prometheus_client import Counter

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize and configure Prometheus instrumentator
Instrumentator().instrument(app).expose(app)

Base.metadata.create_all(bind=engine)

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

# Define a custom metric
submissions_total = Counter('submissions_total', 'Total number of submissions')

@app.post("/submit/")
def submit_text(text: str = Form(...), db: Session = Depends(get_db)):
    new_submission = Submission(text=text)
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    submissions_total.inc()  # Increment the counter
    return {"message": "Submission added"}