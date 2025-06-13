from datetime import timedelta

import os

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from . import models, schemas, auth, tasks
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_role = None
    if user.role_id:
        db_role = db.query(models.Role).filter(models.Role.id == user.role_id).first()
    if not db_role:
        db_role = db.query(models.Role).filter(models.Role.name == "user").first()
        if not db_role:
            db_role = models.Role(name="user")
            db.add(db_role)
            db.commit()
            db.refresh(db_role)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role_id=db_role.id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=schemas.Token)
def login(form: schemas.LoginData, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == form.email).first()
    if not db_user or not auth.verify_password(
        form.password,
        db_user.hashed_password,
    ):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = auth.create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/projects", response_model=schemas.ProjectOut)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    db_project = models.Project(name=project.name, owner_id=current_user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.post("/projects/{project_id}/rfps", response_model=schemas.RFPOut)
def upload_rfp(
    project_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    upload_dir = os.path.join(os.getcwd(), "uploaded_rfps")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    db_rfp = models.RFP(filename=file.filename, project_id=project.id)
    db.add(db_rfp)
    db.commit()
    db.refresh(db_rfp)
    return db_rfp


@router.post("/projects/{project_id}/rfps/{rfp_id}/analyze")
def analyze_rfp(
    project_id: int,
    rfp_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    rfp = db.query(models.RFP).filter(models.RFP.id == rfp_id).first()
    if not project or not rfp or rfp.project_id != project.id or project.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="RFP not found")
    file_path = os.path.join(os.getcwd(), "uploaded_rfps", rfp.filename)
    task = tasks.analyze_rfp.delay(file_path)
    return {"task_id": task.id}
