"""
Resume Analysis Routes - Handles all /api/v1/analyze* endpoints

This file contains the API endpoints that the frontend (Anwar) will call.

Two main endpoints:
1. POST /api/v1/analyze - Analyze resume from text (direct text input)
2. POST /api/v1/analyze/file - Analyze resume from uploaded file (PDF/Word)

Think of routes as "URLs that do something" - when someone visits these URLs,
the corresponding function runs and returns a response.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.models import ResumeAnalysisResponse
from app.services.ai_client import AIClient
from app.services.file_parser import FileParser
from app.config import settings

# Create a router - this is like a "mini app" that holds related endpoints
# Prefix means all routes here will start with /api/v1/analyze
router = APIRouter(prefix="/analyze", tags=["Resume Analysis"])

# Initialize services
# AIClient - talks to Daniyal's AI service
# FileParser - extracts text from PDF/Word files
ai_client = AIClient(settings.ai_service_url)
file_parser = FileParser()


# =============================================================================
# ENDPOINT 1: Analyze from text
# URL: POST /api/v1/analyze
# =============================================================================

@router.post("", response_model=ResumeAnalysisResponse)
async def analyze_resume(
    resume_text: str = Form(...),
    job_description: str = Form(...)
):
    """
    Analyze a resume against a job description.

    This endpoint accepts:
    - resume_text: The raw text content of the resume
    - job_description: The job description to match against

    Both are sent as form data.

    Example curl command:
    curl -X POST "http://localhost:8000/api/v1/analyze" \\
      -F "resume_text=John Doe..." \\
      -F "job_description=Software Engineer..."

    Returns:
        ResumeAnalysisResponse: Analysis results with score, feedback, etc.
    """

    try:
        # ===== Step 1: Validate input =====
        # Make sure resume_text is not just whitespace
        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Resume text cannot be empty"
            )

        # Make sure job_description is not just whitespace
        if not job_description.strip():
            raise HTTPException(
                status_code=400,
                detail="Job description cannot be empty"
            )

        # ===== Step 2: Call AI service =====
        # This is where we send the data to Daniyal's AI for analysis
        analysis = await ai_client.analyze(resume_text, job_description)

        # ===== Step 3: Return results =====
        return analysis

    except HTTPException:
        # Re-raise HTTP exceptions (like 400 Bad Request)
        raise
    except Exception as e:
        # Log the error and return a user-friendly message
        print(f"Analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


# =============================================================================
# ENDPOINT 2: Analyze from uploaded file
# URL: POST /api/v1/analyze/file
# =============================================================================

@router.post("/file", response_model=ResumeAnalysisResponse)
async def analyze_resume_file(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Analyze a resume from an uploaded file (PDF or Word).

    This endpoint accepts:
    - resume: The uploaded file (PDF or DOCX format)
    - job_description: The job description to match against (as form data)

    Example curl command:
    curl -X POST "http://localhost:8000/api/v1/analyze/file" \\
      -F "resume=@/path/to/resume.pdf" \\
      -F "job_description=Software Engineer..."

    How it works:
    1. Receive the uploaded file
    2. Extract text from the file (PDF/Word)
    3. Send extracted text + job description to AI service
    4. Return analysis results

    Returns:
        ResumeAnalysisResponse: Analysis results with score, feedback, etc.
    """

    try:
        # ===== Step 1: Validate job description =====
        if not job_description.strip():
            raise HTTPException(
                status_code=400,
                detail="Job description cannot be empty"
            )

        # ===== Step 2: Extract text from uploaded file =====
        # FileParser will check if file type is supported (PDF/DOCX)
        # and extract the text content
        resume_text = await file_parser.extract_text(resume)

        # Check if we got any text from the file
        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract any text from the uploaded file. "
                       "The file might be empty or corrupted."
            )

        # ===== Step 3: Call AI service =====
        # Send extracted text to Daniyal's AI for analysis
        analysis = await ai_client.analyze(resume_text, job_description)

        # ===== Step 4: Return results =====
        return analysis

    except HTTPException:
        # Re-raise HTTP exceptions (like 400 Bad Request, 500 Server Error)
        raise
    except Exception as e:
        # Log the error and return a user-friendly message
        print(f"File analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"File analysis failed: {str(e)}"
        )


# =============================================================================
# ENDPOINT 3: Get sample response (for testing)
# URL: GET /api/v1/analyze/sample
# =============================================================================

@router.get("/sample", response_model=ResumeAnalysisResponse)
async def get_sample_response():
    """
    Returns a sample analysis response.

    This is useful for:
    - Frontend development before the AI service is ready
    - Testing the API without sending actual data
    - Understanding the response format

    Returns:
        ResumeAnalysisResponse: A fake but realistic analysis result
    """

    return {
        "candidate_name": "John Doe",
        "match_score": 75,
        "verdict": "Good Match",
        "missing_keywords": [
            "kubernetes",
            "CI/CD",
            "microservices"
        ],
        "formatting_errors": [
            "Inconsistent date format",
            "Missing section headers"
        ],
        "actionable_feedback": (
            "Your resume shows strong technical skills, but you're missing "
            "key DevOps keywords that employers want. Add specific examples "
            "of CI/CD pipelines you've built and mention any Kubernetes "
            "deployments. Fix the inconsistent date formatting throughout - "
            "use either 'Jan 2024' or '01/2024' consistently. Consider adding "
            "a Skills section at the top to highlight your core competencies."
        ),
        "ats_approved": True,
        "ats_feedback": (
            "Your resume uses standard formatting and section headers that "
            "most ATS systems can parse correctly. Good use of reverse-"
            "chronological order and clear job titles."
        )
    }
