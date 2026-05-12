from fastapi import HTTPException,FastAPI
from pydantic import BaseModel,Field
from typing import Optional, Annotated, Literal
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

@app.put("/students/{id}")
def updatestudent(id:int,student:UpdatedStudents):
    data=load_data()
    for std in data:
        if std["id"] == id:
            updated_std=student.model_dump(exclude_unset=True)
            std.update(updated_std)
            return JSONResponse(status_code=200,content=std)
    return HTTPException(status_code=404,detail="Student not found")



