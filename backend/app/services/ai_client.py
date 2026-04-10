"""
AI Service Client - Communicates with Daniyal's AI service

This is the bridge between Fardeen's API (this backend) and Daniyal's AI.

CURRENT STATUS: Returns mock data for testing
TODO FOR DANIYAL: Replace the mock response with actual AI API calls

How it works:
1. Receives resume text and job description from the route
2. Sends it to Daniyal's AI service (via HTTP POST)
3. Gets back the analysis results
4. Returns the results to be sent to the frontend
"""

import httpx
from app.models import AIServiceResponse


class AIClient:
    """
    Client for calling the AI analysis service.

    Think of this as a "phone" that your backend uses to call Daniyal's AI.
    Instead of making the AI logic complicated in your routes,
    we keep it separate here so the code stays clean.
    """

    def __init__(self, ai_service_url: str):
        """
        Initialize the AI client.

        Args:
            ai_service_url: The URL where Daniyal's AI service is running
                           (e.g., http://localhost:8001)
        """
        self.ai_service_url = ai_service_url
        # Create an HTTP client for making async requests
        self._client = httpx.AsyncClient(timeout=30.0)

    async def analyze(
        self,
        resume_text: str,
        job_description: str
    ) -> AIServiceResponse:
        """
        Send resume and job description to AI service for analysis.

        This is the main method that routes will call.

        Args:
            resume_text: The text extracted from the uploaded resume
            job_description: The job description to match against

        Returns:
            AIServiceResponse: The analysis results from the AI

        =====================================================================
        TODO FOR DANIYAL:
        Replace the mock response below with this actual API call:

        response = await self._client.post(
            f"{self.ai_service_url}/analyze",
            json={
                "resume_text": resume_text,
                "job_description": job_description
            }
        )
        response.raise_for_status()
        return AIServiceResponse(**response.json())
        =====================================================================
        """

        # ================================================================
        # MOCK RESPONSE - For testing before AI service is ready
        # Daniyal will replace this with actual AI call above
        # ================================================================

        # Simulate processing time (optional, for testing)
        # await asyncio.sleep(0.5)

        # Extract candidate name from resume (simple placeholder)
        candidate_name = self._extract_name(resume_text)

        # Determine verdict based on score
        match_score = 72  # Mock score
        if match_score >= 80:
            verdict = "Strong Match"
        elif match_score >= 60:
            verdict = "Good Match"
        elif match_score >= 40:
            verdict = "Needs Work"
        else:
            verdict = "Poor Match"

        # Return mock analysis result
        return AIServiceResponse(
            candidate_name=candidate_name,
            match_score=match_score,
            verdict=verdict,
            missing_keywords=[
                "cloud infrastructure",
                "agile methodology",
                "system design"
            ],
            formatting_errors=[
                "Inconsistent bullet point formatting",
                "Missing quantifiable achievements"
            ],
            actionable_feedback=(
                "Your resume demonstrates solid technical foundations, "
                "but needs stronger emphasis on measurable impact. "
                "Add specific numbers to your achievements (e.g., 'improved performance by 40%'). "
                "Include any cloud experience (AWS, GCP, Azure) as it's highly valued. "
                "Consider restructuring your projects section to highlight the most relevant work first."
            ),
            ats_approved=True,
            ats_feedback=(
                "Your resume is ATS-friendly. It uses standard section headers "
                "and a clean format that most applicant tracking systems can parse."
            )
        )

    def _extract_name(self, resume_text: str) -> str:
        """
        Simple name extraction from resume text.

        This is a very basic placeholder - it just takes the first line
        if it looks like a name (short enough).

        TODO: Daniyal's AI will do proper NLP-based name extraction.

        Args:
            resume_text: The full resume text

        Returns:
            str: Extracted name or "Unknown Candidate"
        """
        lines = resume_text.strip().split('\n')
        if lines:
            # Assume first non-empty line might contain the name
            first_line = lines[0].strip()
            if len(first_line) < 50:  # Names are usually short
                return first_line
        return "Unknown Candidate"

    async def close(self):
        """
        Close the HTTP client session.
        Should be called when the application shuts down.
        """
        await self._client.aclose()
