from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import upload
from api import download
from api import local_file_api

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


@app.get("/ping")
def ping():
    return {"message": "pong"}

app.include_router(upload.router, prefix='/api/file')
app.include_router(download.router, prefix='/api/file')
app.include_router(local_file_api.router, prefix='/api/file')



