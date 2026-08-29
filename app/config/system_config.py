from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Union, TypedDict, List


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


class InputState(TypedDict):
    """The input state for the graph."""
    user_id: Union[str, None] = None
    session_id: Union[str, None] = None
    ai_respones: Union[str, None] = None
    user_input: Union[str, None] = None
    parsed_memory: Union[str, None] = None
    vector_db_respones: Union[str, None] = None
    memory_condition: Union[List[str], str, None] = None


secret_manager = SystemConfig()
