import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    app_name: str
    environment: str
    database_url: str
    jwt_secret: str
    openai_api_key: str | None
    openai_base_url: str | None
    model_name: str
    log_file: str
    traffic_interval_seconds: float


@lru_cache
def get_settings() -> Settings:
    project_root = Path(__file__).resolve().parents[2]
    load_dotenv(project_root / ".env")
    return Settings(
        app_name=os.getenv("APP_NAME", "IncidentPilot"),
        environment=os.getenv("ENVIRONMENT", "development"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///./incidentpilot.db"),
        jwt_secret=os.getenv("JWT_SECRET", "incidentpilot-local-secret"),
        openai_api_key=os.getenv("OPENAI_API_KEY") or None,
        openai_base_url=os.getenv("OPENAI_BASE_URL") or None,
        model_name=os.getenv("MODEL_NAME", "gpt-5.6"),
        log_file=os.getenv("LOG_FILE", str(Path(__file__).resolve().parents[1] / "application.log")),
        traffic_interval_seconds=float(os.getenv("TRAFFIC_INTERVAL_SECONDS", "5")),
    )
