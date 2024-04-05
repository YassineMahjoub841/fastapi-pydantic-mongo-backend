""" JOB MODELS
Pydantic Model classes relative to the Job object/collection in the database.
"""

# Installed imports
from pydantic import ConfigDict, BaseModel, Field
from bson import ObjectId
from typing import Optional, List, TypeVar 
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator, AfterValidator
from datetime import datetime
from enum import Enum

from beanie import Document
# Local imports
from ..utils import *


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

# Represents a list of unique items.
# It will be represented as a `list[T]` on the model so that it can be serialized to JSON.
# T is the type of the list items
T = TypeVar("T") 
UniqueGenericList = Annotated[list[T], BeforeValidator(validate_unique_list), Field(json_schema_extra={'uniqueItems': True})]

# Represents a list of unique strings.
# It will be represented as a `list[str]` on the model so that it can be serialized to JSON.
UniqueStrList = Annotated[list[str], BeforeValidator(validate_unique_list), Field(json_schema_extra={'uniqueItems': True})]


# Represents the spoken languages required for a Job.
class LanguageEnum(str, Enum):
    en = 'english'
    fr = 'french'
    es = 'spanish'
    it = 'italian'
    ar = 'arabic'
    ja = 'japanese'
    de = 'german'
    ru = 'russian'
    pl = 'polish'
    pt = 'portuguese'
    zh = 'chinese'
    ko = 'korean'
    nl = 'dutch'
    hu = 'hungarian'

# Represents the work model for a Job.
class WorkModelEnum(str, Enum):
    rm = 'remote'
    os = 'on-site'
    hy = 'hybrid'

# Represents the degree required for a Job.
class DegreeEnum(str, Enum):
    associate = 'associate'
    bachelor = 'bachelors'
    master = 'masters'
    phd = 'phd'

# Represents a degree and major required for a Job.
class DegreeModel(BaseModel):
    level: DegreeEnum = Field(description="Minimum degree required")    
    major: Optional[str] = Field(description="Major required", default=None)

# Represents a single Job record.
class JobModel(Document):
    """
    Container for a single Job record.
    """

    # The primary key for the JobModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    #id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(description="Job title")
    degree: DegreeModel = Field(description="Degree & Major required for the Job")
    desc: str = Field(description="Job description & responsibilities")
    skills: UniqueStrList = Field(description="Skillset required for the Job")
    lang: UniqueGenericList[LanguageEnum] = Field(description="Spoken languages required for the Job")
    work_model: WorkModelEnum = Field(description="The Job's work model")
    created : datetime= Field(
        alias="created",
        gt=0,
        description="When the Job was created",
        default_factory=datetime.now,
        exclude=True
    )
    updated : Optional[datetime]= Field(
        alias="updated",
        gt=0,
        description="When the Job was updated",
        default=None,
        exclude=True
    )
    model_config = ConfigDict(
        populate_by_name=True,  
        arbitrary_types_allowed=True,
        json_schema_extra={
        "degree": {
            "level": "associate"
        },
        "desc": "non nisi elit aliqua",
        "lang": [
            "arabic",
            "french",
            "english"
        ],
        "skills": [
            "qui in"
        ],
        "title": "reprehenderit eu",
        "work_model": "remote"
        },
    )
    class Settings:
        name = "jobs"

# Represents a set of optional updates to be made to a Job record.
class UpdateJobModel(BaseModel):

    """
    A set of optional updates to be made to a document in the database.
    """

    title: Optional[str] = None
    degree: Optional[DegreeModel] = None
    desc: Optional[str] = None
    skills: Optional[UniqueStrList] = None
    lang: Optional[UniqueGenericList[LanguageEnum]] = None
    work_model: Optional[WorkModelEnum] = None
    updated: Optional[datetime] = Field(
        alias="updated",
        gt=0,
        description="When the Job was updated",
        default_factory=datetime.now
    )
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "title": "please work (edited again)",
                "degree": {
                    "level": "associate",
                    "major": "string"
                },
                "desc": "string",
                "skills": [
                    "string"
                ],
                "lang": [
                    "english",
                    "arabic"
                ],
                "work_model": "remote"
            }
        },
    )

# Represents a list of `JobModel` instances.
class JobCollection(BaseModel):
    """
    A container holding a list of `JobModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    jobs: List[JobModel]