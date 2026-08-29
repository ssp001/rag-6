from langchain_groq import ChatGroq
from app.config import secret_manager
from app.utils import AiResponesException
import logfire


class ChatGrouqAi:
    def __init__(self):
        self.ai_client = ChatGroq(
            model=secret_manager.Groq_model,
            temperature=0.9,
            max_tokens=None,
            timeout=60,
            max_retries=3,
            api_key=secret_manager.Groq_api_key
            # other params...
        )

    async def run_query(self, query: str, parsed_text: str, parsed_memory: str | None = None):
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
            messages = [
                (
                    "system",
                    f"""You are a helpful assistant.
                    You can read the following document there is score and similiar texts:

                    {parsed_text}

                    also you have memo support it can halp you to get the past conversation with you if it is none you have tp determine the user is new for you {parsed_memory} 
                    
                    and you'r name will be rag-6.
                    if you can't get any {parsed_text} use tools to give user a respones don't faile to to give a respones and staifactory performance for any user.
                    Important:alwayes use tool calling to marge extra knowladge however what parsed text you may get. 
                    Answer the user's question using the document.
                    If the answer cannot be found, use the available tools."""
                ),
                ("human", query),
            ]
            print(parsed_text)
            async for chunk in self.ai_client.astream(input=messages):
                yield chunk.content.encode("utf-8")
        except Exception as error:
            logfire.error(f"Error in AI response: {error}")
            raise AiResponesException(
                f"Error in AI response: {error}") from error
