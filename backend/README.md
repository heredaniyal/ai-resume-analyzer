# Backend API - AI Resume Analyzer

## Quick Start (How to Run)

Open your terminal and run these commands:

```bash
# Navigate to backend folder
cd ai-resume-analyzer/backend

# Make the startup script executable (only needed once)
chmod +x run.sh

# Run the backend server
./run.sh
```

After a few seconds, you'll see:
```
Starting server on http://localhost:8000
API docs available at http://localhost:8000/docs
```

**That's it!** Your API is now running.

---

## Testing the API

### Option 1: Interactive Docs (Easiest)

1. Open your browser
2. Go to http://localhost:8000/docs
3. You'll see all available endpoints
4. Click on any endpoint to try it out

### Option 2: Using curl (Command Line)

**Test health check:**
```bash
curl http://localhost:8000/
```

**Get sample analysis response:**
```bash
curl http://localhost:8000/api/v1/analyze/sample
```

**Analyze resume from text:**
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -F "resume_text=John Doe\nSoftware Engineer\n5 years experience in Python" \
  -F "job_description=Looking for a Python developer with 5+ years experience"
```

**Analyze resume from file (PDF/Word):**
```bash
curl -X POST "http://localhost:8000/api/v1/analyze/file" \
  -F "resume=@/path/to/your/resume.pdf" \
  -F "job_description=Looking for a software engineer"
```

---

## API Endpoints Reference

| Method | Endpoint | What It Does |
|--------|----------|--------------|
| GET | `/` | Basic health check - tells if API is running |
| GET | `/health` | Detailed health status |
| POST | `/api/v1/analyze` | Analyze resume (send as text) |
| POST | `/api/v1/analyze/file` | Analyze resume (upload PDF/Word file) |
| GET | `/api/v1/analyze/sample` | Get fake sample response (for testing) |

---

## What Each File Does

```
backend/
├── app/
│   ├── main.py              # Main application - creates the API app
│   ├── config.py            # Loads settings from .env file
│   ├── models.py            # Defines data shapes (request/response)
│   ├── routes/
│   │   └── analyze.py       # The actual endpoints (URLs that do things)
│   └── services/
│       ├── ai_client.py     # Talks to Daniyal's AI service
│       └── file_parser.py   # Extracts text from PDF/Word files
├── requirements.txt         # List of Python packages needed
├── .env.example            # Template for configuration
├── run.sh                  # One-command startup script
└── README.md               # This file
```

### File Explanations (Beginner-Friendly)

| File | What It Does | When to Edit |
|------|--------------|--------------|
| `main.py` | Creates the API app, sets up CORS, connects routes | Rarely - only for major changes |
| `config.py` | Loads settings like port number | When adding new settings |
| `models.py` | Defines what data looks like (request/response format) | When changing response structure |
| `routes/analyze.py` | **Your main work area** - contains the endpoint logic | Often - when adding/changing endpoints |
| `services/ai_client.py` | Calls Daniyal's AI service | Daniyal will edit this |
| `services/file_parser.py` | Extracts text from uploaded files | When adding new file formats |

---

## Understanding the Flow

Here's what happens when a user uploads a resume:

```
1. User uploads resume.pdf on the website
         │
         ▼
2. Anwar's frontend sends file to YOUR API
   POST /api/v1/analyze/file
         │
         ▼
3. Your backend (file_parser.py) extracts text from PDF
         │
         ▼
4. Your backend (ai_client.py) sends text to Daniyal's AI
         │
         ▼
5. Daniyal's AI analyzes and returns results
         │
         ▼
6. Your backend sends results back to frontend
   { "match_score": 75, "verdict": "Good Match", ... }
```

---

## Team Notes

### For Fardeen (Backend/API - You!)

**Your responsibilities:**
- Maintain the API endpoints in `app/routes/analyze.py`
- Handle file uploads and parsing
- Error handling and validation
- Connect with Daniyal's AI service

**Files you'll edit most:**
- `app/routes/analyze.py` - Add new endpoints, modify logic
- `app/models.py` - Change request/response structure

### For Daniyal (AI Integration)

**Your integration point:** `app/services/ai_client.py`

Replace the mock response in the `analyze()` method with an actual HTTP call to your AI service:

```python
async def analyze(self, resume_text: str, job_description: str):
    response = await self._client.post(
        f"{self.ai_service_url}/analyze",
        json={"resume_text": resume_text, "job_description": job_description}
    )
    response.raise_for_status()
    return AIServiceResponse(**response.json())
```

### For Anwar (Frontend)

**API Base URL:** `http://localhost:8000` (development)

**Main endpoint to use:**
```
POST /api/v1/analyze/file
Content-Type: multipart/form-data

Parameters:
- resume: (file) The PDF or DOCX file
- job_description: (string) The job description text
```

**Example Response:**
```json
{
  "candidate_name": "John Doe",
  "match_score": 75,
  "verdict": "Good Match",
  "missing_keywords": ["kubernetes", "CI/CD"],
  "formatting_errors": ["Inconsistent formatting"],
  "actionable_feedback": "Add more quantifiable achievements...",
  "ats_approved": true,
  "ats_feedback": "Resume is ATS-friendly"
}
```

**CORS:** Already enabled for all origins during development.

---

## Troubleshooting

**Port 8000 already in use:**
```bash
# Change port in .env
API_PORT=8001
```

**Module not found error:**
```bash
# Make sure you're in the backend folder and venv is activated
cd backend
source venv/bin/activate
```

**Can't upload files:**
- Check file size limits in your frontend
- Make sure file is PDF or DOCX format

---

## Next Steps

1. **Run the server** with `./run.sh`
2. **Test endpoints** at http://localhost:8000/docs
3. **Coordinate with team:**
   - Daniyal: Set up your AI service and update `ai_client.py`
   - Anwar: Start calling the API from the frontend
