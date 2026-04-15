# 📄 AI Resume Analyzer — SOFTEC '26

> An AI-powered resume analyzer that scores your resume, identifies skill gaps, checks ATS compatibility, and gives brutally honest feedback — built for the SOFTEC '26 AI Hackathon at FAST-NUCES Lahore.

---

## 🎯 What It Does

Upload your resume PDF and paste a job description. The AI will:

- **Score your resume** out of 100 based on how well it matches the role
- **Identify your strengths** — what you're doing right
- **Find missing keywords** — skills and terms the job requires that you're missing
- **Spot formatting issues** — things that hurt readability and ATS parsing
- **Check ATS compatibility** — whether your resume will pass applicant tracking systems
- **Give actionable feedback** — specific, honest advice to improve your resume

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| AI Model | LLaMA 3.3 70B via Groq API |
| PDF Parsing | pdfplumber |
| Backend API | FastAPI |
| Language | Python 3.10+ |

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/heredaniyal/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Install dependencies

```bash
pip install streamlit groq pdfplumber python-dotenv
```

### 3. Get a free Groq API key

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up / Log in
3. Navigate to **API Keys** → **Create API Key**
4. Copy the key

### 4. Set your API key

**Windows (PowerShell) — permanent:**
```powershell
[System.Environment]::SetEnvironmentVariable("GROQ_API_KEY", "your_key_here", "User")
```
Then restart your terminal.

**Or create a `.env` file inside the `frontend/` folder:**
```
GROQ_API_KEY=your_key_here
```

### 5. Run the app

```bash
cd frontend
python -m streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
ai-resume-analyzer/
│
├── frontend/
│   ├── app.py               # Streamlit UI + Groq AI integration
│   └── .env                 # Your API key (not committed to Git)
│
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application entry point
│   │   ├── config.py        # Environment settings
│   │   ├── models.py        # Request/response data models
│   │   ├── routes/
│   │   │   └── analyze.py   # API endpoints
│   │   └── services/
│   │       ├── ai_client.py     # Groq LLM integration
│   │       └── file_parser.py   # PDF/DOCX text extraction
│   ├── requirements.txt
│   ├── .env.example
│   └── run.sh
│
├── schema.json              # Shared data contract (AI response format)
├── .gitignore
└── README.md
```

---

## 📡 API Response Format

The AI returns structured JSON matching this schema:

```json
{
  "candidate_name": "John Doe",
  "match_score": 78,
  "verdict": "Good Match",
  "strengths": [
    "Strong Python and backend experience",
    "Leadership roles clearly demonstrated"
  ],
  "missing_keywords": ["kubernetes", "CI/CD", "Docker"],
  "formatting_errors": ["Inconsistent date formatting", "Missing professional summary"],
  "actionable_feedback": "Your resume shows solid technical depth but lacks DevOps keywords that this role requires. Add specific examples of deployment pipelines and containerization experience. Quantify your achievements with numbers wherever possible.",
  "ats_approved": true,
  "ats_feedback": "Resume uses standard section headers and clean formatting that ATS systems can parse reliably."
}
```

---

## 👥 Team

| Name | Role |
|------|------|
| **Daniyal** | AI Integration · Prompt Engineering · JSON Schema · Git Management |
| **Fardeen** | Backend API (FastAPI) · File Parsing · Endpoint Design |
| **Anwar** | Frontend UI (Streamlit) · UX Design · Component Layout |

---

## 🏫 Event

Built for **SOFTEC '26 AI Hackathon** — FAST-NUCES Lahore  
6-hour build · April 18, 2026

---

## 📝 Notes

- `.env` files are excluded from Git via `.gitignore` — never commit your API key
- The Groq API free tier is sufficient for demo purposes
- If the real hackathon theme differs from resume analysis, only the system prompt in `frontend/app.py` needs to change — the entire stack stays the same
