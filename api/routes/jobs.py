# local imports
from ..models.JobModels import JobModel, UpdateJobModel, JobCollection
from ..config.mongodb import job_collection
# installed imports
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response
from bson import ObjectId
from pymongo import ReturnDocument


router = APIRouter()


# Endpoints

@router.post(
    "/",
    response_description="Add new Job",
    response_model=JobModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_job(job: JobModel = Body(...)):
    """
    Insert a new job record.

    A unique `id` will be created and provided in the response.
    """
    new_job = await job_collection.insert_one(
        job.model_dump(by_alias=True, exclude=["id"])
    )
    created_job = await job_collection.find_one(
        {"_id": new_job.inserted_id}
    )
    return created_job

@router.get(
    "/",
    response_description="List all jobs",
    response_model=JobCollection,
    response_model_by_alias=False,
)
async def list_jobs():
    """
    List all of the job data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    return JobCollection(jobs=await job_collection.find().to_list(1000))

@router.get(
    "/{id}",
    response_description="Get a single job",
    response_model=JobModel,
    response_model_by_alias=False,
)
async def show_job(id: str):
    """
    Get the record for a specific job, looked up by `id`.
    """
    if (
        job := await job_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return job

    raise HTTPException(status_code=404, detail=f"Job {id} not found")

@router.put(
    "/{id}",
    response_description="Update a job",
    response_model=JobModel,
    response_model_by_alias=False,
)
async def update_job(id: str, job: UpdateJobModel = Body(...)):
    """
    Update individual fields of an existing job record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    job = {
        k: v for k, v in job.model_dump(by_alias=True).items() if v is not None
    }

    if len(job) >= 1:
        update_result = await job_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": job},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Job {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_job := await job_collection.find_one({"_id": id})) is not None:
        return existing_job

    raise HTTPException(status_code=404, detail=f"Job {id} not found")

@router.delete("/{id}", response_description="Delete a job")
async def delete_job(id: str):
    """
    Remove a single job record from the database.
    """
    delete_result = await job_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Job {id} not found")
