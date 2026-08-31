from app.src import AiMemory
from pyresilience import resilient, TimeoutConfig, RetryConfig
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
def ai_memory_search(
    user_chat: str,
    user_id: str
):
    try:
        client = AiMemory()
        client.serach_memory(
            user_id=user_id,
            query=user_chat,
        )
    except AiMemoryException as error:
        raise RuntimeError(
            f"Error in storing memory: {error}") from error
