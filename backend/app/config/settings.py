from pydantic import BaseSettings, Field
from typing import List, Optional
import os

class Settings(BaseSettings):
    """
    Application configuration settings
    """
    # API Configuration
    app_name: str = Field(default="Text Summarization API")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    api_v1_str: str = Field(default="/api/v1")

    # Server Configuration
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    # CORS Configuration
    allowed_origins: List[str] = Field(default=["*"])
    allowed_methods: List[str] = Field(default=["*"])
    allowed_headers: List[str] = Field(default=["*"])

    # File Upload Configuration
    max_file_size: int = Field(default=10 * 1024 * 1024)  # 10MB
    allowed_file_types: List[str] = Field(default=[".txt", ".pdf", ".docx", ".doc"])
    upload_dir: str = Field(default="uploads")

    # Model Configuration
    default_summary_type: str = Field(default="extractive")
    default_summary_length: str = Field(default="medium")
    max_text_length: int = Field(default=50000)  # 50k characters

    # Database Configuration (for future use)
    database_url: Optional[str] = Field(default=None)

    # Logging Configuration
    log_level: str = Field(default="INFO")
    log_file: Optional[str] = Field(default=None)

    # AWS Configuration (for future use)
    aws_region: str = Field(default="us-east-1")
    aws_access_key_id: Optional[str] = Field(default=None)
    aws_secret_access_key: Optional[str] = Field(default=None)
    s3_bucket_name: Optional[str] = Field(default=None)

    # Monitoring Configuration
    enable_metrics: bool = Field(default=True)
    metrics_endpoint: str = Field(default="/metrics")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Create settings instance
settings = Settings()

# Create upload directory if it doesn't exist
if not os.path.exists(settings.upload_dir):
    os.makedirs(settings.upload_dir)