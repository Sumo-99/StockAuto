from fastapi import APIRouter, Request, File, UploadFile, BackgroundTasks,  HTTPException
from fastapi.responses import JSONResponse

from api.helpers.nav_inference_helper import nav_master
from api.database import SessionLocal, engine, Base
from api.models import LocalFile
from api.models_crud.local_file import LocalFileCrud

import os
import uuid

# FastAPI router setup
router = APIRouter()

# SQL Lite DB config and setup
Base.metadata.create_all(bind=engine)
db = SessionLocal()
file_handler = LocalFileCrud()


@router.post("/upload")
async def get_nav(request: Request, tasks: BackgroundTasks,  file: UploadFile = File(...)):
    session_id = str(uuid.uuid4())
    '''
        1. Accept excel file
        2. Run bot.py on it 
        3. Serve back new excel file
    '''

    # Parse request
    form_data = await request.form()
    print("Req Form data --->", form_data)
    row_start = form_data.get('row_start', 4)
    row_end = form_data.get('row_end', 25)
    print("row start: ", row_start, type(row_start))
    print("row end: ", row_end, type(row_end))
    # body_data = await request.body()
    # print("Req Body data --->", body_data)

    # saving file to local
    print("Filedetails")
    print(file.__dict__)
    temp_folder_path = os.path.join(os.getcwd(), f"temp_downloads_{session_id}")
    os.makedirs(temp_folder_path, exist_ok=True)
    file_save_path = os.path.join(temp_folder_path, file.filename)
    with open(file_save_path, "wb") as outfile:
        outfile.write(await file.read())
    
    # Create file obj in DB 
    file_obj = LocalFile(id=str(uuid.uuid4()), status="pending", path=file_save_path)
    created_file = file_handler.create_local_file(db, file_obj)
    
    tasks.add_task(nav_master, created_file.id, file_save_path, row_start, row_end, 2, 5, 8)
    
    response = {
        'status': "Success",
        'message': "NAV calculation in progress",
        'file_id': created_file.id
    }

    return  JSONResponse(content=response)
    # return response