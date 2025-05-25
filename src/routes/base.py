from fastapi import FastAPI,APIRouter,Depends
import os
from helpers.config import get_settings,settings

base_router=APIRouter(
    prefix="/api/v1"
    
)
@base_router.get("/")
async def welcome(app_settings=Depends(get_settings)):
    
    app_name= app_settings.APP_NAME
    app_version=app_settings.APP_VERSION
    return{
        "message":"hello my friend!",
        "app_name": app_name,
        "app_version": app_version
    }