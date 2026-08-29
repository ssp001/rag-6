from pyresilience import resilient, TimeoutConfig, RetryConfig
from app.src import VectorSearch
from app.src import VectorEmbedding
from app.utils.exception_handeler import VectorSearchException


@resilient(
    timeout=TimeoutConfig(
        seconds=60,
    ),
    retry=RetryConfig(
        max_attempts=3,
        delay=10
    ),
)
def qudrent_query_point_search(user_input, user_id, session_id):
    try:
        client = VectorSearch()
        embedding_client = VectorEmbedding()
        embedded_respones = embedding_client.embed_the_docs(text=user_input)
        respones = client.serach_query(
            user_input=embedded_respones,
            user_id=user_id,
            session_id=session_id
        )
        return respones
    except VectorSearchException as error:
        raise RuntimeError(
            f"Error in searching the text in Qdrent: {error}") from error
