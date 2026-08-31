from app.src import AiMemory
from pyresilience import resilient, RetryConfig, TimeoutConfig
from app.utils import AiMemoryException


@resilient(
    timeout=TimeoutConfig(
        seconds=60
    ),
    retry=RetryConfig(
        max_attempts=3,
        delay=10
    )
)
def ai_delete_memory(user_id: str):
    """
    Function to run a query against the AI model using the provided parsed text.
    Args:
        query (str): The user query to be answered.
        parsed_text (str): The text to be used for context in answering the query.
    Returns:
        Generator: A generator yielding chunks of the AI response.
    Raises:
        AiResponesException: If an error occurs during the AI response generation.
    """
    try:
        ai_memory_client = AiMemory()
        respones = ai_memory_client.delete_memory(
            user_id=user_id
        )
        return respones
    except AiMemoryException as error:
        raise RuntimeError(
            f"Error in running the AI query: {error}") from error
