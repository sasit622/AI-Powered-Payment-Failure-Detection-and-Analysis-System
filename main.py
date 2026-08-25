from fastapi import FastAPI,Body,Form,UploadFile,File,Query,Path,APIRouter
from pydantic import BaseModel
from typing import List
from Backend.router.speed_route import router as speed_router 
from Backend.router.user_route import router as user_router
app=FastAPI()
app.include_router(user_router)
app.include_router(speed_router)