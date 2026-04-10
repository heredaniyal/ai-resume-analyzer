"""
Pydantic Models - Defines the shape of data coming in and out of the API

Think of models as "templates" that describe what data should look like.
For example, a ResumeRequest must have resume_text and job_description.

These models are used by FastAPI to:
1. Automatically validate incoming requests
2. Generate API documentation
3. Give helpful error messages if data is wrong
"""

from pydantic import BaseModel, Field
from typing import List


# =============================================================================
# REQUEST MODELS - What the frontend (Anwar) sends to us
# =============================================================================

class ResumeAnalysisRequest(BaseModel):
    """
    What the frontend sends when analyzing a resume.

    Example JSON:
    {
        "resume_text": "John Doe\nSoftware Engineer...",
        "job_description": "Looking for Python developer..."
    }
    """
    resume_text: str = Field(
        ...,
        description="The raw text content extracted from the resume"
    )
    job_description: str = Field(
        ...,
        description="The job description to match the resume against"
    )


# =============================================================================
# RESPONSE MODELS - What we send back to the frontend
# =============================================================================

class ResumeAnalysisResponse(BaseModel):
    """
    The complete analysis result sent back to the frontend.
    Matches the schema.json defined in the project root.

    Example JSON:
    {
        "candidate_name": "John Doe",
        "match_score": 75,
        "verdict": "Strong Match",
        "missing_keywords": ["kubernetes", "CI/CD"],
        "formatting_errors": ["Inconsistent dates"],
        "actionable_feedback": "Add more quantifiable achievements...",
        "ats_approved": true,
        "ats_feedback": "Resume is ATS-friendly"
    }
    """
    candidate_name: str = Field(
        ...,
        description="Name of the candidate extracted from resume"
    )
    match_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Match score between 0-100 (higher is better)"
    )
    verdict: str = Field(
        ...,
        description="Overall verdict like 'Strong Match', 'Needs Work'"
    )
    missing_keywords: List[str] = Field(
        ...,
        description="Important keywords from job description missing in resume"
    )
    formatting_errors: List[str] = Field(
        ...,
        description="List of resume formatting/design issues found"
    )
    actionable_feedback: str = Field(
        ...,
        description="One paragraph of advice on how to improve the resume"
    )
    ats_approved: bool = Field(
        ...,
        description="Whether the resume is ATS (Applicant Tracking System) compatible"
    )
    ats_feedback: str = Field(
        ...,
        description="Explanation of ATS compatibility issues or confirmation"
    )


# =============================================================================
# INTERNAL MODELS - Used for communication with Daniyal's AI service
# =============================================================================

class AIServiceRequest(BaseModel):
    """
    Internal request sent to Daniyal's AI service.
    Same as ResumeAnalysisRequest but kept separate for flexibility.
    """
    resume_text: str
    job_description: str


class AIServiceResponse(BaseModel):
    """
    Internal response received from Daniyal's AI service.
    Same structure as ResumeAnalysisResponse.
    """
    candidate_name: str
    match_score: int
    verdict: str
    missing_keywords: List[str]
    formatting_errors: List[str]
    actionable_feedback: str
    ats_approved: bool
    ats_feedback: str
