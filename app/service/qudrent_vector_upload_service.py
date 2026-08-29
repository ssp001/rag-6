from app.src import QdrentVector
from app.utils import QuadrentVectorException
from .vector_embedding_service import embedde_the_text
from .text_splitter_service import spllitte_the_text
from app.utils import QdrentUploadRespones, json_dump, json_loader
from pyresilience import resilient, TimeoutConfig, RetryConfig
from numpy import array
from typing import List


@resilient(
    timeout=TimeoutConfig(
        seconds=60,
    ),
    retry=RetryConfig(
        max_attempts=3,
        delay=10
    )
)
def upload_embedding_to_db(embeddings: List[array], user_identity, list_of_text: List[str], session_id: str) -> QdrentUploadRespones:
    try:
        vector_db_client = QdrentVector()

        for floats, each_text in zip(embeddings, list_of_text):
            vectors = floats.tolist()
            opration_respones, session_identity = vector_db_client.upload_data(
                vector=vectors,
                user_text=each_text,
                user_id=user_identity,
                session_id=session_id
            )

        model = QdrentUploadRespones(
            session_id=session_identity,
            upload_respones=opration_respones
        )
        return model
    except QuadrentVectorException as error:
        raise RuntimeError(f"Error chunking text: {error}")
