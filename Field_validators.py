

from pydantic import BaseModel, Field
from typing import Annotated,Literal

class Patient(BaseModel):
    patient_id: Annotated[int, Field(gt=0)]
    name: Annotated[str, Field(min_length=3, max_length=50)]
    age: Annotated[int, Field(gt=0, lt=120)]
    gender: Annotated[Literal['male','female','others'], Field()]
    blood_group: Annotated[Literal["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], Field()]
    phone: Annotated[str, Field(min_length=10, max_length=10)]
    disease: Annotated[str, Field(min_length=3)]
    doctor: Annotated[str, Field(min_length=3)]
    admitted: bool
    room_no: Annotated[int, Field(gt=0)]
    medications: Annotated[list[str], Field(min_length=1)]
