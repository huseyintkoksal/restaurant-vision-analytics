"""Application configuration.

All settings are loaded from environment variables (or a local ``.env`` file).
Defaults are deliberately privacy-preserving: demo mode on, raw frame storage
off, short retention window.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application settings.

    Environment variables take precedence over the values defined here. See
    ``.env.example`` for the full list and documentation.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Application ---
    app_name: str = "Restaurant Vision Analytics"
    app_env: str = "development"
    api_prefix: str = "/api"

    # --- Database ---
    database_url: str = "sqlite:///./data/rva.db"

    # --- Demo mode ---
    enable_demo_mode: bool = True
    live_update_interval_seconds: float = 2.0
    # Expected arrivals per simulated minute at baseline. Raise for a busier
    # venue (e.g. fast food); lower for a quiet cafe. Demo/visual only.
    demo_arrival_rate: float = 16.0
    # Optional seed for reproducible demo runs (None = varied each start).
    demo_seed: int | None = 7

    # --- Privacy hard-defaults ---
    # Raw frame/video persistence is OFF by default and must be an explicit,
    # audited operator decision to enable.
    enable_raw_frame_storage: bool = False
    data_retention_days: int = 7

    # --- Tracking (ephemeral, anonymous) ---
    track_ttl_seconds: float = 5.0

    # --- Camera (optional; demo mode needs none) ---
    camera_source: str | None = None

    # --- CORS ---
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_cors(cls, value: object) -> object:
        """Allow a comma-separated string (env var) or a real list."""
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @property
    def is_demo(self) -> bool:
        return self.enable_demo_mode

    @property
    def privacy_summary(self) -> dict[str, bool]:
        """Machine-readable summary surfaced through the API and dashboard."""
        return {
            "facial_recognition": False,
            "biometric_identification": False,
            "demographic_inference": False,
            "emotion_detection": False,
            "audio_recording": False,
            "persistent_customer_tracking": False,
            "raw_frame_storage": self.enable_raw_frame_storage,
        }


@lru_cache
def get_settings() -> Settings:
    """Return a cached :class:`Settings` instance."""
    return Settings()
