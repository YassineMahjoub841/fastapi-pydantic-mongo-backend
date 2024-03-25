from fastapi import FastAPI
from api.routes.jobs import router as JobsRouter
from contextlib import asynccontextmanager
from api.config.mongodb import initiate_database




@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This is an async context manager function called `lifespan` that takes one parameter `app` of type FastAPI. 
    It launches the database by calling `initiate_database` asynchronously and then yields the control back.
    """
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
    """
    Get the root endpoint of the API.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return {"message": "Welcome to this fantastic app."}


#Include routers
app.include_router(JobsRouter, tags=["Jobs"], prefix="/jobs")
