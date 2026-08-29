from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from numpy import ndarray
from qdrant_client.http.models.models import UpdateResult
from uuid import UUID


class PdfLoderRespoens(BaseModel):
    text: List[str] = None


class TextSplitterRespones(BaseModel):
    chunked_text: List[str] = None


class VectorEmbeddingRespones(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    embeddings: List[ndarray] = None


class QdrentUploadRespones(BaseModel):
    upload_respones: UpdateResult = None
    session_id: UUID = None


class QdrentDeleteRespones(BaseModel):
    upload_respones: UpdateResult = None


class VectorSearchRespones(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    search_respones: Optional[List[dict["score":int, "payload":str]]] = None
