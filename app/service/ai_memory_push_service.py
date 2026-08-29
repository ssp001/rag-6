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
def ai_memory_push(
    ai_respoones: str,
    user_chat: str,
    user_id: str,
    session_id: str
):
    try:
        client = AiMemory()
        client.store_memory(
            user_id=user_id,
            user_chat=user_chat,
            session_id=session_id,
            ai_respoones=ai_respoones
        )
    except AiMemoryException as error:
        raise RuntimeError(
            f"Error in storing memory: {error}") from error
