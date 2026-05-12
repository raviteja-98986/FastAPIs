from fastapi import HTTPException,FastAPI
from pydantic import BaseModel,Field
from typing import Optional, Annotated, Literal

from rest_framework import status
from starlette.responses import JSONResponse
import json



def load_data():
    with open('student.json','r') as f:
        data = json.load(f)
        return data

class Students(BaseModel):
    id:Annotated[int,Field(...,description="Student ID")]
    name:Annotated[str,Field(...,description="Student Name")] = ""
    age:Annotated[int,Field(...,gt=0,lt=100,description="Student Age")]
    branch:Annotated[Literal['CSE','IT','ECE','EEE','CIVIL','MECH'],Field(...,description="Student Branch")]

class UpdatedStudents(BaseModel):
    id:Annotated[Optional[int],Field(...,description="Student ID")]=None
    name:Annotated[Optional[str],Field(...,description="Student Name")] =None
    age:Annotated[Optional[int],Field(...,gt=0,lt=100,description="Student Age")]=None
    branch:Annotated[Optional[Literal['CSE','IT','ECE','EEE','CIVIL','MECH']],Field(...,description="Student Branch")]=None

app=FastAPI()

@app.get('/')
def get_students():
    data = load_data()
    return JSONResponse(status_code=status.HTTP_200_OK,content=data)

@app.get('/students/{id}')
def get_student(id: int):
    data = load_data()
    for std in data:
        if std['id'] == id:
            return JSONResponse(status_code=200,content=std)
    return HTTPException(status_code=404,detail="Student not found")

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
@app.put("/students/{id}")
def updatestudent(id:int,student:UpdatedStudents):
    data=load_data()
    for std in data:
        if std["id"] == id:
            updated_std=student.model_dump(exclude_unset=True)
            std.update(updated_std)
            return JSONResponse(status_code=200,content=std)
    return HTTPException(status_code=404,detail="Student not found")

@app.delete('/students/{id}')
def delete_student(id:int):
    data=load_data()
    for std in data:
        if std["id"] == id:
            del std
            return JSONResponse(status_code=200,content={"message": "Student deleted successfully"})
    return HTTPException(status_code=404,detail="Student not found")

