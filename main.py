from fastapi import FastAPI

from Backend.router.analysis import router as analysis_router

app = FastAPI()

app.include_router(analysis_router)
from Backend.router.agent_route import router as agent_router
from Backend.router.analysis import router as analysis_router
#from Backend.router.user_route import router as user_router
from Backend.router.speed_route import router as speed_router

app = FastAPI()

app.include_router(agent_router)
app.include_router(analysis_router)
#app.include_router(user_router)
app.include_router(speed_router)