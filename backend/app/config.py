"""
Application configuration
Loads environment variables and provides settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables"""

    # API Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"

    # AI Service Configuration (for Daniyal's AI component)
    ai_service_url: str = os.getenv("AI_SERVICE_URL", "http://localhost:8001")

# Global settings instance
settings = Settings()
