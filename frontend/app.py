import streamlit as st
import pdfplumber
import asyncio
from groq import AsyncGroq
import json
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.markdown("""
    <style>
        .main-title { font-size: 42px; font-weight: 700; color: #4F8BF9; text-align: center; }
        .sub-title { font-size: 18px; color: #888888; text-align: center; margin-bottom: 30px; }
        .score-box { background-color: #1E1E2E; border-radius: 15px; padding: 30px;
                     text-align: center; border: 2px solid #4F8BF9; }
        .score-number { font-size: 72px; font-weight: 800; color: #4F8BF9; }
        .section-header { font-size: 20px; font-weight: 600; color: #4F8BF9; margin-top: 20px; }
        .tip-box { background-color: #1E1E2E; border-left: 4px solid #4F8BF9;
                   padding: 12px 16px; border-radius: 8px; margin-bottom: 10px; color: #CCCCCC; }
        [data-testid="stFileUploaderDropzoneInstructions"] div span { display: none !important; }
        [data-testid="stFileUploaderDropzoneInstructions"] div::after {
            content: "10MB per file • PDF"; font-size: 14px; color: #888888; }
    </style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/942/942748.png", width=80)
    st.markdown("## 📄 Resume Analyzer")
    st.markdown("---")
    st.markdown("### How it works:")
    st.markdown("1. 📤 Upload your resume PDF")
    st.markdown("2. 📝 Paste the job description")
    st.markdown("3. 🤖 AI reads and analyzes it")
    st.markdown("4. 📊 Get your score out of 100")
    st.markdown("5. 💡 See tips to improve")
    st.markdown("---")
    st.markdown("### What we check:")
    st.markdown("- ✅ Professional Summary")
    st.markdown("- ✅ Work Experience")
    st.markdown("- ✅ Skills & Keywords")
    st.markdown("- ✅ Education")
    st.markdown("- ✅ Formatting & ATS")
    st.markdown("---")
    st.caption("Built for SOFTEC'26 AI Hackathon")
    st.caption("Team: Anwar | Fardeen | Daniyal")

# ── Title ─────────────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">📄 AI Resume Analyzer</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Upload your resume and get an AI-powered score with actionable feedback</p>', unsafe_allow_html=True)
st.markdown("---")

# ── Groq call ────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a brutally honest expert resume analyst.
Analyze the resume against the job description and return ONLY valid JSON, nothing else.

{
  "candidate_name": "string",
  "match_score": integer (0-100),
  "verdict": "Strong Match | Good Match | Needs Work | Poor Match",
  "strengths": ["up to 4 specific strengths found in the resume"],
  "missing_keywords": ["up to 5 missing keywords or skills"],
  "formatting_errors": ["up to 4 formatting issues"],
  "actionable_feedback": "one dense honest paragraph of improvement advice",
  "ats_approved": true or false,
  "ats_feedback": "one sentence on ATS compatibility"
}"""

async def analyze_resume(resume_text: str, job_description: str) -> dict:
    client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"RESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{job_description or 'Not provided. Evaluate resume quality generally.'}"}
        ],
        temperature=0.3,
        max_tokens=1024,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

def extract_pdf_text(uploaded_file) -> str:
    with pdfplumber.open(uploaded_file) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

# ── Main UI ───────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    uploaded_file = st.file_uploader(
        label="📤 Drop your Resume here (PDF only)",
        type=["pdf"],
        help="Make sure your file is in PDF format. Max size: 10MB"
    )
    st.caption("📎 PDF only · Maximum file size: 10MB")

    job_description = st.text_area(
        "📋 Paste Job Description (optional but recommended)",
        height=150,
        placeholder="Paste the job posting here to get a match score tailored to this specific role..."
    )

    if uploaded_file is not None:
        if uploaded_file.size > 10 * 1024 * 1024:
            st.error("❌ File too large. Maximum allowed is 10MB.")
        else:
            st.success(f"✅ **{uploaded_file.name}** uploaded successfully!")

            if st.button("🔍 Analyze Resume", use_container_width=True, type="primary"):
                with st.spinner("🤖 AI is reading your resume..."):
                    try:
                        resume_text = extract_pdf_text(uploaded_file)
                        result = asyncio.run(analyze_resume(resume_text, job_description))

                        st.markdown("---")

                        # Score
                        score = result.get("match_score", 0)
                        verdict = result.get("verdict", "")
                        verdict_emoji = {"Strong Match": "🌟", "Good Match": "⭐", "Needs Work": "⚠️", "Poor Match": "❌"}.get(verdict, "")
                        ats_badge = "✅ ATS Friendly" if result.get("ats_approved") else "❌ Not ATS Friendly"

                        st.markdown('<p class="section-header">📊 Your Resume Score</p>', unsafe_allow_html=True)
                        st.markdown(f"""
                            <div class="score-box">
                                <div class="score-number">{score}<span style="font-size:32px;color:#888">/100</span></div>
                                <div style="color:#4F8BF9;font-size:20px;margin-top:8px;">{verdict} {verdict_emoji}</div>
                                <div style="color:#888;font-size:14px;margin-top:6px;">{ats_badge} · {result.get("ats_feedback", "")}</div>
                            </div>
                        """, unsafe_allow_html=True)

                        st.markdown("---")

                        # Strengths & Issues
                        left, right = st.columns(2)
                        with left:
                            st.markdown('<p class="section-header">✅ Strengths</p>', unsafe_allow_html=True)
                            for s in result.get("strengths", []):
                                st.markdown(f'<div class="tip-box">{s}</div>', unsafe_allow_html=True)

                        with right:
                            st.markdown('<p class="section-header">⚠️ Areas to Improve</p>', unsafe_allow_html=True)
                            for e in result.get("formatting_errors", []):
                                st.markdown(f'<div class="tip-box">{e}</div>', unsafe_allow_html=True)
                            for k in result.get("missing_keywords", []):
                                st.markdown(f'<div class="tip-box">Missing keyword: <b>{k}</b></div>', unsafe_allow_html=True)

                        st.markdown("---")

                        # Actionable feedback
                        st.markdown('<p class="section-header">💡 Actionable Feedback</p>', unsafe_allow_html=True)
                        st.markdown(f'<div class="tip-box">{result.get("actionable_feedback", "")}</div>', unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")
    else:
        st.markdown("###")
        st.markdown("""
            <div style="text-align:center;padding:60px 20px;border:2px dashed #4F8BF9;
                        border-radius:15px;color:#888;">
                <div style="font-size:60px;">📄</div>
                <div style="font-size:22px;margin-top:10px;color:#CCCCCC;">
                    Upload your resume to get started
                </div>
                <div style="font-size:14px;margin-top:8px;">
                    Supports PDF format only · Max 10MB
                </div>
            </div>
        """, unsafe_allow_html=True)