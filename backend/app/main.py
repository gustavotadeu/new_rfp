from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from . import routes, auth, models
from .database import SessionLocal

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.on_event("startup")
def create_default_admin():
    """Create an initial admin user if none exists."""
    db = SessionLocal()
    try:
        admin_role = (
            db.query(models.Role).filter(models.Role.name == "admin").first()
        )
        if not admin_role:
            admin_role = models.Role(name="admin")
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)

        exists = (
            db.query(models.User)
            .filter(models.User.email == "admin@example.com")
            .first()
        )
        if not exists:
            db_user = models.User(
                username="admin",
                email="admin@example.com",
                hashed_password=auth.get_password_hash("admin"),
                role_id=admin_role.id,
            )
            db.add(db_user)
            db.commit()
    finally:
        db.close()


@app.get("/")
def read_root(current_user: models.User = Depends(auth.get_current_user)):
    return {"message": f"Hello, {current_user.username}"}


app.include_router(routes.router)
