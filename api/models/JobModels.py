from pydantic import ConfigDict, BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List, TypeVar , Union
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator, AfterValidator

from enum import Enum
from ..utils import *

_unix_ts = dict(example=get_time())
"""Common attributes for all Unix timestamp fields"""

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

T = TypeVar("T")
UniqueGenericList = Annotated[list[T], BeforeValidator(validate_unique_list), Field(json_schema_extra={'uniqueItems': True})]


# Represents a list of unique strings.
# It will be represented as a `list[str]` on the model so that it can be serialized to JSON.
UniqueStrList = Annotated[list[str], BeforeValidator(validate_unique_list), Field(json_schema_extra={'uniqueItems': True})]
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
class WorkModelEnum(str, Enum):
    rm = 'remote'
    os = 'on-site'
    hy = 'hybrid'
class DegreeEnum(str, Enum):
    associate = 'associate'
    bachelor = 'bachelors'
    master = 'masters'
    phd = 'phd'
class DegreeModel(BaseModel):
    level: DegreeEnum = Field(description="Minimum degree required")    
    major: Optional[str] = Field(description="Major required", default=None)
class JobModel(BaseModel):
    """
    Container for a single Job record.
    """

    # The primary key for the JobModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(description="Job title")
    degree: DegreeModel = Field(description="Degree & Major required for the Job")
    desc: str = Field(description="Job description & responsibilities")
    skills: UniqueStrList = Field(description="Skillset required for the Job")
    lang: UniqueGenericList[LanguageEnum] = Field(description="Spoken languages required for the Job")
    work_model: WorkModelEnum = Field(description="The Job's work model")

    created : Union[int, float]= Field(
        alias="created",
        gt=0,
        description="When the Job was created (Unix timestamp)",
        json_schema_extra=_unix_ts
    )
    updated : Union[int, float] = Field(
        alias="updated",
        gt=0,
        description="When the Job  was updated for the last time (Unix timestamp)",
        json_schema_extra=_unix_ts
    )
    model_config = ConfigDict(
        populate_by_name=True,  
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
        "title": "reprehenderit eu",
        "degree": {
          "degree": "associate"
        },
        "desc": "non nisi elit aliqua",
        "skills": [
          "qui in"
        ],
        "lang": [
        "arabic","french","english"
        ],
        "work_model": "remote",
        "created": 95704773.096542,
        "updated": 15550303.247843325
      }
        },
    )
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
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": 3.0,
            }
        },
    )
class JobCollection(BaseModel):
    """
    A container holding a list of `JobModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    jobs: List[JobModel]