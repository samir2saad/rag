from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
import os
from models import ResponseSignal
from helpers.config import get_settings,settings
from controllers import DataController,ProjectController
import aiofiles
import logging

logger = logging.getLogger('uvicorn.error')


data_router=APIRouter(
    prefix="/api/v1/data"
    
)
@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str , file:UploadFile,
                  app_settings=Depends(get_settings)    ):
    data_controller=DataController()
    is_valid ,result_signal=data_controller.validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":result_signal
            }
        )
    

    project_file_path, file_id=data_controller.generate_unique_name(
        orig_file_name=file.filename,
        project_id=project_id
    )
    try:
        async with aiofiles.open(project_file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:

        logger.error(f"Error while uploading file: {e}")

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        )

    return JSONResponse(
            content={
                "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                "file_id": file_id
            }
        )