from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ats import evaluate_resume_against_jd, input_pdf_text

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/evaluate/", response_class=HTMLResponse)
async def evaluate_resume(
    request: Request, file: UploadFile = File(...), job_description: str = Form(...)
):
    resume_text = input_pdf_text(file.file)
    ats_evaluation = evaluate_resume_against_jd(resume_text, job_description)
    evaluation = eval(ats_evaluation)  # Convert string to dictionary
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "jd_match": evaluation.get("JD Match", ""),
            "missing_keywords": evaluation.get("MissingKeywords", []),
            "profile_summary": evaluation.get("Profile Summary", ""),
        },
    )
