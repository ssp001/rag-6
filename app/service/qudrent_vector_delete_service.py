from app.src import QdrentVector
from app.utils import QuadrentVectorException
from app.utils import json_dump, QdrentDeleteRespones
from uuid import UUID
from pyresilience import resilient, TimeoutConfig, RetryConfig


@resilient(
    timeout=TimeoutConfig(
        seconds=60,
    ),
    retry=RetryConfig(
        max_attempts=3,
        delay=10
    )
)
def delete_embedding_from_db(user_identity: str, session_indentity: str) -> QdrentDeleteRespones:
    try:
        vector_db_client = QdrentVector()

        respones = vector_db_client.delete_vectors(
            user_id=user_identity,
            session_id=session_indentity
        )
        model = QdrentDeleteRespones(
            upload_respones=respones
        )
        return model
    except QuadrentVectorException as error:
        raise RuntimeError(f"Error chunking text: {error}")
