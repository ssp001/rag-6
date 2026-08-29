from mem0 import MemoryClient
from app.config import secret_manager
import logfire
from app.utils import AiMemoryException
from mem0.client.types import AddMemoryOptions, SearchMemoryOptions
import datetime


class AiMemory:
    def __init__(self):
        self.client = MemoryClient(
            api_key=secret_manager.memo_api,
        )

    def store_memory(self, ai_respoones, user_chat, user_id: str, session_id):

        messages = [
            {"role": "user", "content": user_chat},
            {"role": "assistant", "content": ai_respoones}
        ]
        try:
            self.client.add(
                messages=messages,
                user_id="alice",
                options=AddMemoryOptions(
                    filters={
                        "user_id": user_id,
                        "session_id": session_id
                    },
                    timestamp=datetime.datetime(),
                    infer=True
                ),

            )
            logfire.info(f"memory updated for this user:{user_id} sucessfully")
        except Exception as error:
            logfire.error(f"Error storing memory: {error}")
            raise AiMemoryException(f"Error storing memory: {error}")

    def serach_memory_fregments(self, query: str, user_id: str, session_id):
        try:
            result = self.client.search(
                user_id=user_id,
                query=query,
                options=SearchMemoryOptions(
                    filters={
                        "user_id": user_id,
                        "session_id": session_id
                    },
                    top_k=10,
                ),
                limit=5
            )

            logfire.info(f"memory search sucessfully")
            return result["memory"]
        except Exception as error:
            logfire.error(f"Error searching memory: {error}")
            raise AiMemoryException(f"Error searching memory: {error}")
