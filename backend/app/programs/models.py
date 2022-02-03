from typing import Optional
import uuid
from pydantic import BaseModel, Field
import datetime


class ProgramModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    completed: bool = False
    img_url: str = Field(...)
    program_details: str = Field(...)
    is_active: bool = True
    start_date: datetime.date
    end_date: datetime.date
    purpose:str = Field(...)
    status:str = Field(...)
    report_required: bool = False
    scorecard_required: bool = False
    show_report: bool = False
    show_scorecard: bool = True
    price: int = None
    product: int = Field()

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "name": "My important task",
                "completed": True,
            }
        }


class UpdateProgramModel(BaseModel):
    name: Optional[str]
    completed: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "name": "My important task",
                "completed": True,
            }
        }