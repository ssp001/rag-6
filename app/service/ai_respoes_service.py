from app.src import ChatGrouqAi
from pyresilience import resilient, TimeoutConfig, RetryConfig


@resilient(
    timeout=TimeoutConfig(
        seconds=60
    ),
    retry=RetryConfig(
        max_attempts=3,
        delay=10
    )
)
async def ai_run_query(query, parsed_text, memory_input):
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
        ai_client = ChatGrouqAi()
        async for chunk in ai_client.run_query(
                query=query,
                parsed_text=parsed_text,
                parsed_memory=memory_input
        ):
            yield chunk
    except Exception as error:
        raise RuntimeError(
            f"Error in running the AI query: {error}") from error
