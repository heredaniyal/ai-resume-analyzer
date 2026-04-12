# AI Resume Analyzer - Complete System Map

> **Beginner-friendly explanation of how everything connects**

---

## 📊 Visual Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER VISITS WEBSITE                             │
│                    (Anwar's Frontend - React/Next.js)                   │
│                                                                         │
│   ┌───────────────────────────────────────────────────────────────┐    │
│   │  User sees:                                                    │    │
│   │  - Upload button for resume (PDF/Word)                        │    │
│   │  - Text area for job description                              │    │
│   │  - "Analyze My Resume" button                                 │    │
│   └───────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ User uploads resume.pdf
                                   │ and clicks "Analyze"
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 1: Frontend sends HTTP POST request                               │
│                                                                         │
│  URL: POST /api/v1/analyze/file                                         │
│  Body (multipart/form-data):                                            │
│    - resume: [binary file data]                                         │
│    - job_description: "Software Engineer position..."                   │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ Over the internet (HTTP)
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 2: Fardeen's Backend API Receives Request                         │
│  (FastAPI server running on port 8000)                                  │
│                                                                         │
│  File: backend/app/routes/analyze.py                                    │
│  Function: analyze_resume_file()                                        │
│                                                                         │
│  What happens:                                                          │
│  1. ✅ Validate job description is not empty                            │
│  2. ✅ Check file type is PDF or DOCX                                   │
│  3. ✅ Pass file to FileParser service                                  │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 3: File Parser Extracts Text                                      │
│  File: backend/app/services/file_parser.py                              │
│                                                                         │
│  If PDF:                                                                │
│    - PyPDF2 reads the PDF                                               │
│    - Extracts text from each page                                       │
│    - Returns: "John Doe\nSoftware Engineer\n5 years..."                 │
│                                                                         │
│  If Word (.docx):                                                       │
│    - python-docx reads the document                                     │
│    - Extracts text from paragraphs                                      │
│    - Returns: "John Doe\nSoftware Engineer\n5 years..."                 │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ Now we have plain text
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 4: AI Client Sends to Daniyal's AI Service                        │
│  File: backend/app/services/ai_client.py                                │
│  Function: ai_client.analyze(resume_text, job_description)              │
│                                                                         │
│  What happens:                                                          │
│  1. Creates HTTP POST request                                           │
│  2. Sends to: http://localhost:8001/analyze (Daniyal's service)         │
│  3. Payload: {                                                          │
│       "resume_text": "John Doe...",                                     │
│       "job_description": "Software Engineer..."                         │
│     }                                                                   │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ HTTP request to Daniyal's AI
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 5: Daniyal's AI Service Analyzes                                  │
│  (Separate Python service running on port 8001)                         │
│                                                                         │
│  What the AI does:                                                      │
│  1. Extract candidate name using NLP                                    │
│  2. Compare resume skills vs job requirements                           │
│  3. Calculate match score (0-100)                                       │
│  4. Identify missing keywords                                           │
│  5. Check formatting issues                                             │
│  6. Check ATS compatibility                                             │
│  7. Generate actionable feedback                                        │
│                                                                         │
│  Returns:                                                               │
│  {                                                                      │
│    "candidate_name": "John Doe",                                        │
│    "match_score": 75,                                                   │
│    "verdict": "Good Match",                                             │
│    "missing_keywords": ["kubernetes", "CI/CD"],                         │
│    "formatting_errors": ["Inconsistent dates"],                         │
│    "actionable_feedback": "...",                                        │
│    "ats_approved": true,                                                │
│    "ats_feedback": "..."                                                │
│  }                                                                      │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ JSON response back to Fardeen's API
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 6: Backend Sends Result to Frontend                               │
│                                                                         │
│  HTTP Response: 200 OK                                                  │
│  Content-Type: application/json                                         │
│  Body: The analysis result from Step 5                                  │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ Over the internet (HTTP)
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 7: Frontend Displays Results to User                              │
│  (Anwar's React/Next.js code)                                           │
│                                                                         │
│  What user sees:                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  ✅ Match Score: 75/100                                          │   │
│  │  ✅ Verdict: Good Match                                          │   │
│  │                                                                  │   │
│  │  ⚠️ Missing Keywords:                                            │   │
│  │     • kubernetes                                                 │   │
│  │     • CI/CD                                                      │   │
│  │                                                                  │   │
│  │  ❌ Formatting Errors:                                           │   │
│  │     • Inconsistent dates                                         │   │
│  │                                                                  │   │
│  │  ✅ ATS Approved: Yes                                            │   │
│  │                                                                  │   │
│  │  💡 Feedback: Add more quantifiable achievements...              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure (Complete)

```
ai-resume-analyzer/
│
├── backend/                          # FARADEEN'S RESPONSIBILITY
│   ├── app/
│   │   ├── main.py                   # Main FastAPI application
│   │   ├── config.py                 # Settings (port, AI service URL)
│   │   ├── models.py                 # Data shapes (request/response)
│   │   ├── routes/
│   │   │   └── analyze.py            # API endpoints (YOUR MAIN WORK)
│   │   └── services/
│   │       ├── file_parser.py        # PDF/Word → text extraction
│   │       └── ai_client.py          # Calls Daniyal's AI (integration point)
│   ├── requirements.txt              # Python packages
│   ├── .env.example                  # Configuration template
│   ├── run.sh                        # Startup script
│   └── README.md                     # Backend documentation
│
├── ai-service/                       # DANIYAL'S RESPONSIBILITY
│   ├── main.py                       # AI service (Flask/FastAPI)
│   ├── analyzer.py                   # AI analysis logic
│   ├── llm_integration.py            # Calls GPT-4/Claude API
│   ├── requirements.txt              # Python packages for AI
│   └── README.md                     # AI service documentation
│
├── frontend/                         # ANWAR'S RESPONSIBILITY
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadForm.tsx        # Resume upload component
│   │   │   ├── Results.tsx           # Display analysis results
│   │   │   └── ...
│   │   ├── pages/
│   │   │   └── index.tsx             # Main page
│   │   └── api/
│   │       └── client.ts             # Calls Fardeen's backend API
│   ├── package.json
│   └── README.md                     # Frontend documentation
│
├── schema.json                       # Shared data contract (all 3 agree on this)
├── README.md                         # Project overview
└── HOW_IT_WORKS.md                   # This file

```

---

## 🔗 How The Three Parts Connect

### Connection 1: Frontend → Backend (Anwar ↔ Fardeen)

```
┌──────────────┐         HTTP POST          ┌──────────────┐
│   Frontend   │ ──────────────────────────▶ │   Backend    │
│   (Anwar)    │                             │  (Fardeen)   │
│  React/Next  │                             │   FastAPI    │
│   port 3000  │                             │   port 8000  │
└──────────────┘                             └──────────────┘

What Anwar sends:
  POST http://localhost:8000/api/v1/analyze/file
  Content-Type: multipart/form-data
  
  Form data:
    - resume: [file upload]
    - job_description: "Software Engineer..."

What Fardeen's API sends back:
  Status: 200 OK
  Content-Type: application/json
  
  {
    "candidate_name": "John Doe",
    "match_score": 75,
    "verdict": "Good Match",
    "missing_keywords": ["kubernetes"],
    "formatting_errors": ["Inconsistent dates"],
    "actionable_feedback": "...",
    "ats_approved": true,
    "ats_feedback": "..."
  }
```

**What Anwar needs from Fardeen:**
1. API URL: `http://localhost:8000` (development) or production URL
2. Endpoint: `POST /api/v1/analyze/file`
3. Response format (see `backend/app/models.py`)

**What Fardeen needs to tell Anwar:**
- CORS is already enabled (allows frontend to call API)
- Use `/api/v1/analyze/sample` for testing with fake data

---

### Connection 2: Backend → AI Service (Fardeen ↔ Daniyal)

```
┌──────────────┐         HTTP POST          ┌──────────────┐
│   Backend    │ ──────────────────────────▶ │  AI Service  │
│  (Fardeen)   │                             │   (Daniyal)  │
│   FastAPI    │                             │   Flask/Fast │
│   port 8000  │                             │   port 8001  │
└──────────────┘                             └──────────────┘

What Fardeen's backend sends:
  POST http://localhost:8001/analyze
  Content-Type: application/json
  
  {
    "resume_text": "John Doe\nSoftware Engineer...",
    "job_description": "Looking for Python developer..."
  }

What Daniyal's AI sends back:
  Status: 200 OK
  Content-Type: application/json
  
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

**What Daniyal needs to do:**

1. Create an AI service (can be Flask or FastAPI)
2. Implement `/analyze` endpoint that accepts `resume_text` and `job_description`
3. Call LLM API (OpenAI GPT-4 or Anthropic Claude) for analysis
4. Return response in the exact format above

**Current placeholder in Fardeen's code:**

File: `backend/app/services/ai_client.py`

```python
async def analyze(self, resume_text: str, job_description: str):
    # TODO: Daniyal replaces this with actual API call:
    
    response = await self._client.post(
        f"{self.ai_service_url}/analyze",
        json={
            "resume_text": resume_text,
            "job_description": job_description
        }
    )
    response.raise_for_status()
    return AIServiceResponse(**response.json())
```

---

## 🚀 What Happens Next (Step by Step)

### Phase 1: Backend Working (Fardeen - You)

```bash
# 1. Install dependencies
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Create .env file
cp .env.example .env

# 3. Run the server
./run.sh
```

**Test it works:**
```bash
# Visit in browser
http://localhost:8000/docs

# Or test with curl
curl http://localhost:8000/api/v1/analyze/sample
```

---

### Phase 2: AI Service Working (Daniyal)

Daniyal needs to:

1. **Create the AI service folder:**
```bash
cd ai-resume-analyzer
mkdir ai-service
cd ai-service
```

2. **Create basic AI service:**

```python
# ai-service/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import anthropic  # or openai

app = FastAPI()

class AIRequest(BaseModel):
    resume_text: str
    job_description: str

@app.post("/analyze")
async def analyze(req: AIRequest):
    # Call Claude API for analysis
    client = anthropic.Client(api_key="...")
    
    prompt = f"""
    Analyze this resume against the job description.
    
    Resume:
    {req.resume_text}
    
    Job Description:
    {req.job_description}
    
    Return JSON with:
    - candidate_name
    - match_score (0-100)
    - verdict
    - missing_keywords (list)
    - formatting_errors (list)
    - actionable_feedback
    - ats_approved (boolean)
    - ats_feedback
    """
    
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Parse response and return JSON
    return parse_response(response.content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

3. **Run AI service on port 8001**

4. **Update Fardeen's config:**
   - In `backend/.env`, set `AI_SERVICE_URL=http://localhost:8001`

---

### Phase 3: Frontend Working (Anwar)

Anwar needs to:

1. **Create frontend (React/Next.js example):**

```bash
cd ai-resume-analyzer
npx create-next-app frontend
cd frontend
```

2. **Create upload form component:**

```tsx
// frontend/src/components/UploadForm.tsx
export default function UploadForm() {
  const [resume, setResume] = useState<File | null>(null);
  const [jobDesc, setJobDesc] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_description", jobDesc);
    
    const response = await fetch("http://localhost:8000/api/v1/analyze/file", {
      method: "POST",
      body: formData,
    });
    
    const data = await response.json();
    setResult(data);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="file" onChange={(e) => setResume(e.target.files[0])} />
      <textarea onChange={(e) => setJobDesc(e.target.value)} />
      <button type="submit">Analyze</button>
      
      {result && (
        <div>
          <h2>Score: {result.match_score}/100</h2>
          <p>Verdict: {result.verdict}</p>
          <p>ATS Approved: {result.ats_approved ? "Yes" : "No"}</p>
        </div>
      )}
    </form>
  );
}
```

3. **Run frontend on port 3000:**
```bash
npm run dev
```

---

## 🧪 Testing The Full Flow

### Test 1: Backend Only (Fardeen can test now)

```bash
# 1. Start backend
cd backend && ./run.sh

# 2. Test sample endpoint (no AI needed)
curl http://localhost:8000/api/v1/analyze/sample

# 3. Test with text input
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -F "resume_text=John Doe\nSoftware Engineer" \
  -F "job_description=Python developer needed"
```

You'll get mock data back (from `ai_client.py`).

---

### Test 2: Backend + AI (Fardeen + Daniyal)

```bash
# Terminal 1: Start AI service
cd ai-service
python main.py  # Runs on port 8001

# Terminal 2: Start backend
cd backend
./run.sh  # Runs on port 8000

# Terminal 3: Test full flow
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -F "resume_text=John Doe\n5 years Python experience" \
  -F "job_description=Senior Python developer"
```

You'll get real AI analysis back.

---

### Test 3: Full Stack (All 3 together)

```bash
# Terminal 1: AI service
cd ai-service && python main.py

# Terminal 2: Backend
cd backend && ./run.sh

# Terminal 3: Frontend
cd frontend && npm run dev

# Browser: Visit http://localhost:3000
# Upload resume, enter job description, click Analyze
```

---

## 📋 Shared Data Contract (schema.json)

All three team members must agree on this format:

```json
{
  "candidate_name": "String",
  "match_score": "Integer (0-100)",
  "verdict": "String (e.g., 'Strong Match', 'Needs Work')",
  "missing_keywords": ["List", "of", "missing", "keywords"],
  "formatting_errors": ["List", "of", "formatting", "issues"],
  "actionable_feedback": "String (paragraph of advice)",
  "ats_approved": "Boolean",
  "ats_feedback": "String (ATS compatibility explanation)"
}
```

This is defined in:
- `backend/app/models.py` (Fardeen)
- `ai-service/` (Daniyal - must return this format)
- `frontend/src/types.ts` (Anwar - expects this format)

---

## 🎯 Your Next Steps (Fardeen)

### Immediate (Today):

1. **Run the backend locally:**
   ```bash
   cd backend
   ./run.sh
   ```

2. **Test the endpoints:**
   - Visit http://localhost:8000/docs
   - Try the `/api/v1/analyze/sample` endpoint
   - Try uploading a PDF with `/api/v1/analyze/file`

3. **Coordinate with Daniyal:**
   - Share the expected AI service format (see Connection 2 above)
   - Agree on the port (8001) and endpoint (`/analyze`)

4. **Coordinate with Anwar:**
   - Share the API documentation URL
   - Let him know CORS is enabled
   - Show him the `/sample` endpoint for testing

### This Week:

1. Wait for Daniyal to set up AI service
2. Update `ai_client.py` to call his real service
3. Test the full backend → AI flow
4. Help Anwar debug any frontend → backend issues

---

## 🆘 Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| Port 8000 already in use | Change `API_PORT` in `.env` |
| CORS error from frontend | Already enabled, check URL is correct |
| File upload fails | Check file is PDF or DOCX, not image |
| AI service not responding | Check `AI_SERVICE_URL` in `.env` |
| Module not found | Activate venv: `source venv/bin/activate` |

---

## 📞 Team Communication Checklist

### Fardeen tells Daniyal:
- [ ] AI service should run on port 8001
- [ ] Endpoint: `POST /analyze`
- [ ] Request format: `{ resume_text, job_description }`
- [ ] Response format: see schema.json

### Fardeen tells Anwar:
- [ ] Backend API runs on port 8000
- [ ] Main endpoint: `POST /api/v1/analyze/file`
- [ ] Use `/sample` for testing with fake data
- [ ] CORS is enabled

### Daniyal tells Fardeen:
- [ ] AI service is running
- [ ] Here's the URL to call
- [ ] Here's how to handle errors

### Anwar tells Fardeen:
- [ ] Frontend is calling the API
- [ ] Here's any error I'm seeing
- [ ] Need new endpoint for X feature

---

## 🎓 Learning Resources

### FastAPI (Your Backend):
- Official docs: https://fastapi.tiangolo.com/tutorial/
- File uploads: https://fastapi.tiangolo.com/tutorial/request-files/

### AI Integration (For Daniyal):
- Anthropic Claude API: https://docs.anthropic.com/claude/docs
- OpenAI GPT API: https://platform.openai.com/docs

### Frontend API Calls (For Anwar):
- Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- Axios: https://axios-http.com/docs/intro

---

**Good luck with the project! 🚀**
