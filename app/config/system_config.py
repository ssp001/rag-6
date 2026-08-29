from pydantic_settings import BaseSettings, SettingsConfigDict


class SystemConfig(BaseSettings):
    """System configuration settings."""
    qdrent_api: str
    qdrent_endpoint: str
    qdrent_collection_name: str
    Logfier_key: str
    Logfier_project: str
    Embedding_model: str
    memo_api: str
    Groq_model: str
    Groq_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


secret_manager = SystemConfig()
