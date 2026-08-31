from app.utils import AiMemoryException
from app.config import secret_manager
from mem0 import MemoryClient
import logfire


class AiMemory:
    def __init__(self):
        self.client = MemoryClient(
            api_key=secret_manager.memo_api,
        )

    def add_memory(self, user_chat, user_id: str):

        messages = [
            {"role": "user", "content": user_chat},
        ]
        try:
            respones = self.client.add(
                messages=messages,
                user_id=user_id
            )
            logfire.info(f"memory updated for this user:{user_id} sucessfully")
            return respones
        except Exception as error:
            logfire.error(f"Error storing memory: {error}")
            raise AiMemoryException(f"Error storing memory: {error}")

    def serach_memory(self, query: str, user_id: str):
        try:

            result = self.client.search(
                query=query,
                filters={
                    "user_id": user_id
                }
            )

            logfire.info(f"memory search sucessfully")
            return result
        except Exception as error:
            logfire.error(f"Error searching memory: {error}")
            raise AiMemoryException(f"Error searching memory: {error}")

    def delete_memory(self, user_id: str):
        try:
            respoens = self.client.delete_all(
                user_id=user_id
            )
            logfire.info(
                f"memory delete operation succesfull for user_id:{user_id}")
            return respoens["message"]
        except Exception as error:
            logfire.warning(
                f"deleteation opration for user_id:{user_id} failed")
            logfire.error(str(error))
            raise AiMemoryException(str(errors=error)) from error
