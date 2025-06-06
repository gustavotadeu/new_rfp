from fastapi import FastAPI, Depends

from . import routes, auth, models

app = FastAPI()


@app.get("/")
def read_root(current_user: models.User = Depends(auth.get_current_user)):
    return {"message": f"Hello, {current_user.username}"}


app.include_router(routes.router)
