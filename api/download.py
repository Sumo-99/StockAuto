from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path

import uuid
import json
import base64
import shutil
import os
import time

from api.local_file_api import get_file as get_file_data

router = APIRouter()

def clear_folder(file_path):
    path = os.path.dirname(file_path)
    if os.path.exists(path):
        print(f"Will commence deletion for {file_path} in 2 mins...")
        time.sleep(120) 
        shutil.rmtree(path)
    else:
        print(f"{file_path} is clear. Nothing to clean up...")
    print(f"Deletion for {path} completed")

@router.get("/download/{file_id}")
def download_file(file_id: str, tasks: BackgroundTasks):
    session_id = str(uuid.uuid4())

    # Get file by file_id
    file_data_response = get_file_data(file_id=file_id)  
    if file_data_response.status_code != 200:
        raise HTTPException(status_code=file_data_response.status_code, detail=file_data_response.content.decode())
    
    # print("file data raw repsonse --->", file_data_response)
    # print("file data parsed repsonse --->", json.loads(file_data_response.body))
    file_data_response = json.loads(file_data_response.body)

    # Check if the file exists
    dir_path = os.path.dirname(file_data_response["path"])
    file_path = Path(os.path.join(dir_path, 'nav_updated_file.xlsx')) # This file name is hardcoded in the nav_inference_helper.py script
    print("File_path: ", file_path)

    if not os.path.exists(dir_path):
        return JSONResponse(content = {
            'status': 'failure',
            'message': 'file not found on server'
        }, status_code = 404)
        # raise HTTPException(status_code=404, detail="File not found")
    
    # Check File State and return appropriate response
    file_status = file_data_response["status"]
    print("file status --->", file_status)
    if file_status == "pending":
        return JSONResponse(content = {
            'status': file_status,
            'message': 'Please try after sometime. File is being processed...'
        }, status_code = 200)
    elif file_status == "failure":
        # File Cleanup
        tasks.add_task(clear_folder, file_path)
    
        return JSONResponse(content = {
            'status': file_status,
            'message': 'File processing failed. Please re-upload and try again...'
        }, status_code = 500)
    else:
        response_data = dict()
        response_data["status"] = file_status
        response_data["message"] = "File processed successfully. Download in progress..."

        # Encode file content as base64
        with open(file_path, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode('utf-8')
        response_data["data"] = {"file": encoded_string}

        # File Cleanup
        tasks.add_task(clear_folder, file_path)

        return JSONResponse(content=response_data)
