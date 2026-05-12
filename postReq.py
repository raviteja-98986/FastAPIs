import json

from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from typing import Optional, Annotated, Literal

from starlette.responses import JSONResponse


def load_data():
    with open('student.json','r') as f:
        data = json.load(f)
        return data
def save_data(data):
    with open('student.json','w') as f:
        json.dump(data,f)

class Students(BaseModel):
    id:Annotated[int,Field(...,description="Student ID")]
    name:Annotated[str,Field(...,description="Student Name")] = ""
    age:Annotated[int,Field(...,gt=0,lt=100,description="Student Age")]
    branch:Annotated[Literal['CSE','IT','ECE','EEE','CIVIL','MECH'],Field(...,description="Student Branch")]

app = FastAPI()

@app.post('/create')
def create_student(student: Students):
    data = load_data()

    # Check if student ID already exists
    for s in data:
        if s["id"] == student.id:
            raise HTTPException(status_code=409,detail="student already exists")

    data.append(student.model_dump())
    save_data(data)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Student created successfully",
            "student": student.model_dump()
        }
    )

