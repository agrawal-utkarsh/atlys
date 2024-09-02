from fastapi import FastAPI, Depends, HTTPException, status
from app.routers import router
from app.auth import verify_token

app = FastAPI()

app.include_router(router, dependencies=[Depends(verify_token)])

@app.get("/")
def read_root():
    return {"message": "Welcome!"}
