"""
AI Resume Analyzer - Backend API
Main FastAPI application entry point

This is the first file that runs when the server starts.
It creates the FastAPI app and configures all the settings.

Think of this as the "main entrance" to your API building.
All requests come through here and get directed to the right place.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import analyze
from app.config import settings


# =============================================================================
# Create the FastAPI Application
# =============================================================================

app = FastAPI(
    title="AI Resume Analyzer API",
    description="""
## AI Resume Analyzer

This API analyzes resumes against job descriptions and provides:
- **Match Score**: How well the resume matches the job (0-100)
- **Missing Keywords**: Important terms from the job description
- **Formatting Errors**: Issues with resume layout/structure
- **ATS Check**: Whether the resume is Applicant Tracking System friendly
- **Actionable Feedback**: Specific advice to improve the resume

### Team
- **Backend/API**: Fardeen
- **AI Service**: Daniyal
- **Frontend**: Anwar
    """,
    version="1.0.0"
)


# =============================================================================
# Configure CORS (Cross-Origin Resource Sharing)
# =============================================================================

# CORS allows the frontend (running on a different domain/port) to call this API
# Without this, browsers would block requests from Anwar's frontend

app.add_middleware(
    CORSMiddleware,
    # In production, replace ["*"] with specific origins like:
    # ["https://yourdomain.com", "https://www.yourdomain.com"]
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Allows all headers (Authorization, Content-Type, etc.)
)


# =============================================================================
# Include API Routes
# =============================================================================

# This connects the analyze routes (in app/routes/analyze.py) to the main app
# All routes in that file will be prefixed with /api/v1
app.include_router(analyze.router, prefix="/api/v1", tags=["Analysis"])


# =============================================================================
# Basic Endpoints (Health Checks)
# =============================================================================

@app.get("/")
async def root():
    """
    Root endpoint - basic health check.

    Visit http://localhost:8000 to see this.
    """
    return {
        "status": "ok",
        "message": "AI Resume Analyzer API is running",
        "docs": "Visit /docs for interactive API documentation"
    }


@app.get("/health")
async def health_check():
    """
    Detailed health check endpoint.

    This can be used by monitoring systems to check if the service is healthy.
    Visit http://localhost:8000/health
    """
    return {
        "status": "healthy",
        "service": "api",
        "version": "1.0.0",
        "debug_mode": settings.debug
    }


# =============================================================================
# Run the Server (when executed directly)
# =============================================================================

if __name__ == "__main__":
    import uvicorn

    # uvicorn.run() starts the web server
    # app.main:app means "run the 'app' variable from app/main.py"
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,      # Usually 0.0.0.0 (all interfaces)
        port=settings.api_port,      # Usually 8000
        reload=settings.debug        # Auto-reload on code changes (dev only)
    )
