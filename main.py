from fastapi import FastAPI,Body,Form,UploadFile,File,Query,Path,APIRouter
from pydantic import BaseModel
from typing import List
from src.router.user_route import router as user_router
app=FastAPI()
app.include_router(user_router)

class User(BaseModel):
    exists:bool

class ResUser(BaseModel):
    category:str
    interest:str
    recom:List[str]
dic=[
    {"name":"Sasi","age":10,"city":"chennai"},
    {"name":"Annu","age":20,"city":"bangalore"},
]
@app.get("/")
def read_root():
    return {"Message": "First Api"}

@app.get("/name")
def read_name():
    return {"Message": "Sasi"}

@app.post("/recomand")
def recomand(user:User):
    age=user.age
    cate=''
    if age >18:
        cate="Adult"
    else:
        cate="Minor"
    if user.city.lower()=="che":
        r=['basketball','beach','travel']
    else:
        r=['swimming','mall']
    return{
        "category":'hello',
        "interest":cate,
        "recom":r,
    }

@app.post("/text")
def text(content:str=Body(...,media_type="text/plain")):
    return{
        'type':"Plain Typess",
        'text':content
    }


@app.post("/form")
def form_data(username:str=Form(...),password:str=Form(...)):
    return{
        "type":"Form Data",
        "user":username,
        "pass":password
    }
@app.post("/files")
def upload_files(file: UploadFile = File(...)):
    return{
        "type":"File Upload",
        "filename": file.filename,
        "content_type": file.content_type
    }

#Query validation
@app.get("/dispaly")
def get_value(age:int=Query(ge=10,le=100)):
    for val in dic:
        if val["age"]==age:
            return val
    return {"message":"No user found"}

#Path Validation 
@app.get("/display/{age}/{name}")
def get_path(age:int=Path(ge=10,le=100),name:str=Path(min_length=3,max_length=10,pattern="^[A-Za-z]")):
    for val in dic:
        if val["age"]==age and val["name"].lower()==name.lower():
            return val
    return {"message":"No user founds"}

@app.post("/img-upload")
async def img_upload(file:UploadFile = File(...)):
    path = "D:\\tmp\\fastapi-project\\src\\fastapi_project\\img\\" + file.filename
    with open(path,"wb") as f:
        f.write(await file.read())
    return {
        "message":"File Uploaded Sucessfully"
    }