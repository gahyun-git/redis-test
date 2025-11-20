from fastapi import FastAPI
from .routers import users, events, jobs

app = FastAPI()

app.include_router(users.router)
app.include_router(events.router)
app.include_router(jobs.router)

@app.get("/")
async def root():
    return {"message": "Redis FastAPI Test"}