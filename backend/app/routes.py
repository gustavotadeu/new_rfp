from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas, auth
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
