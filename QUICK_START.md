# Quick Reference - AI Resume Analyzer

> One-page cheat sheet for the team

---

## 🏃 Run Everything Locally

```bash
# Terminal 1 - Daniyal's AI Service
cd ai-service
python main.py                    # Runs on http://localhost:8001

# Terminal 2 - Fardeen's Backend
cd backend
./run.sh                          # Runs on http://localhost:8000

# Terminal 3 - Anwar's Frontend  
cd frontend
npm run dev                       # Runs on http://localhost:3000
```

---

## 📡 API Endpoints Cheat Sheet

### Fardeen's Backend (Port 8000)

| Endpoint | Method | What it does |
|----------|--------|--------------|
| `/` | GET | Health check |
| `/docs` | GET | Interactive API docs (Swagger UI) |
| `/api/v1/analyze` | POST | Analyze resume from **text** |
| `/api/v1/analyze/file` | POST | Analyze resume from **file** (PDF/Word) |
| `/api/v1/analyze/sample` | GET | Get fake sample response |

### Daniyal's AI Service (Port 8001)

| Endpoint | Method | What it does |
|----------|--------|--------------|
| `/analyze` | POST | Analyze resume text (called by Fardeen's backend) |

---

## 📦 Data Format (All Must Use This)

### Request to AI Service
```json
{
  "resume_text": "John Doe\nSoftware Engineer...",
  "job_description": "Looking for Python developer..."
}
```

### Response from AI Service (and Backend to Frontend)
```json
{
  "candidate_name": "John Doe",
  "match_score": 75,
  "verdict": "Good Match",
  "missing_keywords": ["kubernetes", "CI/CD"],
  "formatting_errors": ["Inconsistent dates"],
  "actionable_feedback": "Add more quantifiable achievements...",
  "ats_approved": true,
  "ats_feedback": "Resume is ATS-friendly"
}
```

---

## 🔗 Connection Map (Simplified)

```
┌─────────────┐      HTTP POST      ┌─────────────┐      HTTP POST      ┌─────────────┐
│   Frontend  │ ───────────────────▶ │   Backend   │ ───────────────────▶ │  AI Service │
│   (Anwar)   │   port 3000 → 8000  │  (Fardeen)  │   port 8000 → 8001  │  (Daniyal)  │
│  React/Next │                     │   FastAPI   │                     │   Flask/Fast│
└─────────────┘                     └─────────────┘                     └─────────────┘
       ▲                                    │                                    │
       │                                    │                                    │
       │         ┌──────────────────────────┘                                    │
       │         │   Returns JSON response                                       │
       │         ▼                                                               │
       │  ┌─────────────┐                                                        │
       └──│  Displays   │                                                        │
          │   Results   │                                                        │
          └─────────────┘                                                        │
                                                                                 │
          ┌──────────────────────────────────────────────────────────────────────┘
          │   Calls LLM API (OpenAI/Anthropic)
          ▼
     ┌──────────┐
     │   LLM    │
     │  (Cloud) │
     └──────────┘
```

---

## 🧪 Test Commands

### Test Backend is Running
```bash
curl http://localhost:8000/
# Expected: {"status":"ok","message":"AI Resume Analyzer API is running"}
```

### Test Sample Response (No AI Needed)
```bash
curl http://localhost:8000/api/v1/analyze/sample
```

### Test Full Analysis (With Text)
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -F "resume_text=John Doe\nSoftware Engineer with 5 years Python experience" \
  -F "job_description=Looking for senior Python developer"
```

### Test File Upload
```bash
curl -X POST "http://localhost:8000/api/v1/analyze/file" \
  -F "resume=@/path/to/resume.pdf" \
  -F "job_description=Software Engineer position"
```

---

## 📁 Who Owns What?

| Person | Responsibility | Files to Edit | Runs On |
|--------|---------------|---------------|---------|
| **Fardeen** | Backend API | `backend/app/routes/analyze.py` | Port 8000 |
| **Daniyal** | AI Service | `ai-service/main.py` | Port 8001 |
| **Anwar** | Frontend UI | `frontend/src/` | Port 3000 |

---

## ⚙️ Configuration Files

### Backend (.env)
```bash
AI_SERVICE_URL=http://localhost:8001   # Daniyal's service
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
```

### AI Service (if using .env)
```bash
# API keys for LLM providers
ANTHROPIC_API_KEY=sk-...
# or
OPENAI_API_KEY=sk-...
```

### Frontend (if using .env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🐛 Troubleshooting

| Error | Fix |
|-------|-----|
| `Connection refused` on port 8000 | Run `./run.sh` in backend folder |
| `Connection refused` on port 8001 | Start Daniyal's AI service |
| CORS error in browser console | Check backend URL in frontend code |
| Module not found | Run `pip install -r requirements.txt` |
| Port already in use | Change port in `.env` or kill existing process |

---

## ✅ Integration Checklist

### Fardeen + Daniyal
- [ ] Daniyal's AI service responds to `POST /analyze`
- [ ] Response format matches schema.json
- [ ] Fardeen updates `AI_SERVICE_URL` in backend `.env`
- [ ] Test: Backend → AI call works

### Fardeen + Anwar
- [ ] Anwar knows the API URL (port 8000)
- [ ] Anwar can access `/docs` for API reference
- [ ] Frontend can call `/api/v1/analyze/file`
- [ ] CORS is working (enabled by default)

### Full Stack
- [ ] All 3 services running (ports 3000, 8000, 8001)
- [ ] Upload resume on frontend → see results
- [ ] Error handling works at each step

---

## 📞 Quick Team Sync Points

**Before starting:**
1. Agree on data format (schema.json)
2. Agree on ports (8000, 8001, 3000)
3. Share this document with team

**During development:**
1. Fardeen: Backend ready, share `/docs` URL
2. Daniyal: AI service ready, test with curl
3. Anwar: Frontend ready, test API calls

**Before demo:**
1. Test full flow end-to-end
2. Prepare sample resume and job description
3. Decide who presents which part

---

For detailed explanations, see `HOW_IT_WORKS.md`
