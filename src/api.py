import time
import uuid

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

from src import main as ai_grade
from src.config import logger


app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def create_upload_file(file: UploadFile = File(...), theme: str = Form(...)):
    logger.info(f">>> theme: {theme}")

    file_id = str(uuid.uuid4())

    file_path = f"storage/{file_id}.pdf"

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    ai_grade.main(theme, file_path)
    
    time.sleep(5)

    return {"filename": file_id}
