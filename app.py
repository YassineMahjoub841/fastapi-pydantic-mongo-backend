from fastapi import FastAPI
from api.routes.jobs import router as JobsRouter
from contextlib import asynccontextmanager
from api.config.mongodb import initiate_database




@asynccontextmanager
async def lifespan(app: FastAPI):
    #Launch database
    await initiate_database()
    yield

app = FastAPI(
    title="Job Posting API",
    summary="An MVP-sized application using FastAPI to add a ReST API to a MongoDB 'Jobs' collection.",
    lifespan=lifespan
)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app."}

app.include_router(JobsRouter, tags=["Jobs"], prefix="/jobs")
