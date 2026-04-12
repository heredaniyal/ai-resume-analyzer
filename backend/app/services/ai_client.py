"""
AI Service Client - Calls Groq LLM directly for resume analysis.
No separate AI microservice needed — this calls Groq inline.

Setup:
    pip install groq
    Set GROQ_API_KEY in your .env file
    Get free key at: https://console.groq.com
"""

import json
import os
from groq import AsyncGroq
from app.models import AIServiceResponse


SYSTEM_PROMPT = """You are a brutally honest, expert resume analyst and hiring consultant.
Analyze the provided resume against the job description and return ONLY a valid JSON object.
No preamble, no markdown, no explanation — raw JSON only.

JSON structure to return:
{
  "candidate_name": "Full name extracted from resume, or 'Unknown Candidate'",
  "match_score": <integer 0-100>,
  "verdict": "<one of: 'Strong Match', 'Good Match', 'Needs Work', 'Poor Match'>",
  "missing_keywords": ["keyword1", "keyword2", "...up to 6 items"],
  "formatting_errors": ["error1", "error2", "...up to 5 items"],
  "actionable_feedback": "One dense, honest paragraph of specific advice to improve this resume for this role.",
  "ats_approved": <true or false>,
  "ats_feedback": "One sentence on ATS compatibility."
}

Scoring guide:
- 80-100: Strong match, most requirements met
- 60-79:  Good match, some gaps
- 40-59:  Needs significant work
- 0-39:   Poor fit for this role
"""


class AIClient:

    def __init__(self, ai_service_url: str = ""):
        # ai_service_url param kept for compatibility with Fardeen's routes
        # We don't use it — Groq is called directly
        self._client = AsyncGroq(
            api_key=os.environ.get("GROQ_API_KEY")
        )

    async def analyze(
        self,
        resume_text: str,
        job_description: str
    ) -> AIServiceResponse:

        user_message = f"""RESUME:
{resume_text}

---

JOB DESCRIPTION:
{job_description if job_description.strip() else "No job description provided. Evaluate resume quality generally."}
"""

        response = await self._client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Fast, free on Groq
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,      # Low temp = consistent, structured output
            max_tokens=1024,
            response_format={"type": "json_object"}  # Forces JSON output
        )

        raw = response.choices[0].message.content
        data = json.loads(raw)

        return AIServiceResponse(
            candidate_name=data.get("candidate_name", "Unknown Candidate"),
            match_score=int(data.get("match_score", 0)),
            verdict=data.get("verdict", "Needs Work"),
            missing_keywords=data.get("missing_keywords", []),
            formatting_errors=data.get("formatting_errors", []),
            actionable_feedback=data.get("actionable_feedback", ""),
            ats_approved=bool(data.get("ats_approved", False)),
            ats_feedback=data.get("ats_feedback", "")
        )

    async def close(self):
        await self._client.aclose()