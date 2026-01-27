from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
import shutil
from datetime import datetime

router = APIRouter(prefix="/api/files", tags=["files"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a single file"""
    try:
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "filename": filename,
            "original_filename": file.filename,
            "content_type": file.content_type,
            "size": os.path.getsize(file_path)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-multiple")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """Upload multiple files"""
    uploaded_files = []
    
    for file in files:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{file.filename}"
            file_path = os.path.join(UPLOAD_DIR, filename)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            uploaded_files.append({
                "filename": filename,
                "original_filename": file.filename,
                "size": os.path.getsize(file_path)
            })
        except Exception as e:
            uploaded_files.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return {"files": uploaded_files}

@router.get("/list")
async def list_files():
    """List all uploaded files"""
    files = []
    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        files.append({
            "filename": filename,
            "size": os.path.getsize(file_path),
            "created": datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
        })
    return {"files": files}
