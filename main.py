from fastapi import FastAPI, Path, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated, Literal
import json

app = FastAPI()


class Patient(BaseModel):
    patient_id: Annotated[str, Field(gt=0)]
    name: Annotated[str, Field(min_length=3, max_length=50)]
    age: Annotated[int, Field(gt=0, lt=120)]
    gender: Annotated[Literal['male', 'female', 'others'], Field()]
    blood_group: Annotated[
        Literal["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
        Field()
    ]
    phone: Annotated[str, Field(min_length=10, max_length=10)]
    disease: Annotated[str, Field(min_length=3)]
    doctor: Annotated[str, Field(min_length=3)]
    admitted: bool
    room_no: Annotated[int, Field(gt=0)]
    medications: Annotated[list[str], Field(min_length=1)]


def load_data():
    with open("patients.json", "r") as f:
        return json.load(f)


def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)


@app.post("/patients")
def create(patient_info: Patient):

    data = load_data()

    patient_id = patient_info.patient_id

    if patient_id not in data:

        data[patient_id] = patient_info.model_dump(
            exclude={"patient_id"}
        )

        save_data(data)

        return JSONResponse(
            status_code=201,
            content={
                "msg": "Patient created successfully"
            }
        )

    return JSONResponse(
        status_code=409,
        content={
            "msg": "Patient already exists"
        }
    )