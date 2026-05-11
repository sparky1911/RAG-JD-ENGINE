from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File

from app.models import JobRequest
from app.rag import analyze_job
from app.ingest import ingest_resume


app = FastAPI()


@app.get("/")
def home():

    return {
        "status": "running"
    }


@app.post("/analyze-job")
def analyze(data: JobRequest):

    res = analyze_job(
        data.job_description
    )

    return {
        "result": res
    }


@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...)
):

    file_path = (
        "app/resume/resume.pdf"
    )

    contents = await file.read()

    with open(file_path, "wb") as f:

        f.write(contents)

    ingest_resume()

    return {
        "message":
        "Resume uploaded successfully"
    }