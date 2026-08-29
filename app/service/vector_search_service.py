from app.src import VectorSearch
from app.utils import VectorSearchException, VectorSearchRespones
from pyresilience import resilient, TimeoutConfig, RetryConfig
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
def search_in_db(query: str, user_id: str, session_id: str) -> list[str]:
    """
    Function to split the text into chunks and build embeddings for each chunk.
    """
    try:
        vector_serach_client = VectorSearch()
        parsed_db_text = vector_serach_client.serach_query(
            user_input=query,
            user_id=user_id,
            session_id=session_id
        )
        return parsed_db_text
    except VectorSearchException as error:
        raise RuntimeError(
            f"Error in searching the text in db: {error}")
