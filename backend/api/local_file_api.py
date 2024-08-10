from fastapi import APIRouter, Request, File, UploadFile, BackgroundTasks,  HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from api.helpers.nav_inference_helper import nav_master
from api.database import SessionLocal, engine, Base
from api.models import LocalFile
from api.models_crud.local_file import LocalFileCrud

import uuid


# FastAPI router setup
router = APIRouter()

# SQL Lite DB config and setup
Base.metadata.create_all(bind=engine)
db = SessionLocal()
file_handler = LocalFileCrud()

@router.get("/{file_id}")
def get_file(file_id: str):
    file = file_handler.get_local_file(file_id, db)
    response = {
        'file_id': file.id,
        'status': file.status,
        'path': file.path,
        'deletion_queued': file.deletion_queued
    }
    return JSONResponse(content=response)

@router.post("/create_file")
async def create_file(request: Request):
    request_body = await request.json()
    status = request_body.get('status', 'pending')
    path = request_body.get('path', 'nil_path')

    file_obj = LocalFile(id=str(uuid.uuid4()), status=status, path=path)
    created_file = file_handler.create_local_file(db, file_obj)


    return JSONResponse(content = {
        'status': 'success',
        'message': 'File created successfully',
        'file_id': created_file.id
    })

@router.put("/update_file/{file_id}")
async def update_file(file_id: str, request: Request):
    request_body = await request.json()
    status = request_body.get('status')
    path = request_body.get('path')
    deletion_queued = request_body.get('deletion_queued')
    print("deletion_queued", deletion_queued)

    # if not status or not path:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Status and path are required fields."
    #     )

    try:
        updated_file = file_handler.update_local_file(file_id, db, status, path, deletion_queued)
        return {"message": "File updated successfully", "file": updated_file}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error occurred.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")