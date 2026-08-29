import logfire
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import secret_manager
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from app.utils import VectorSearchException
from qdrant_client import QdrantClient
from qdrant_client.models import (
    FieldCondition,
    Filter,
    MatchValue
)

from qdrant_client.models import (
    MatchValue,
    Filter,
    FieldCondition
)
from typing import List, Union


class VectorSearch:
    def __init__(self):
        try:
            self.client = QdrantClient(
                api_key=secret_manager.qdrent_api,
                url=secret_manager.qdrent_endpoint,
                cloud_inference=True,
                timeout=60
            )

            if self.client.collection_exists(
                collection_name=secret_manager.qdrent_collection_name
            ):
                emedding_model = HuggingFaceEmbeddings(
                    model_name=secret_manager.Embedding_model
                )
                self.qudrent_client = QdrantVectorStore.from_existing_collection(
                    url=secret_manager.qdrent_endpoint,
                    api_key=secret_manager.qdrent_api,
                    collection_name=secret_manager.qdrent_collection_name,
                    retrieval_mode=RetrievalMode.DENSE,
                    embedding=emedding_model,
                    content_payload_key="text"
                )
        except Exception as error:
            logfire.error(
                f"Error initializing QdrantVectorStore: {error}")
            raise VectorSearchException(
                f"Error initializing QdrantVectorStore: {error}") from error

    def serach_query(self, user_input: str, user_id: str, session_id: str) -> List[str]:
        """
        Search for similar text in the Qdrant collection based on the user input.
        Args:
            user_input (str): The input text to search for similar content.
        Returns:
            str: The most similar text found in the Qdrant collection.
        Raises:
            VectorSearchException: If an error occurs during the search operation.
        """
        try:
            results = self.qudrent_client.similarity_search(
                query=user_input,
                filter=Filter(
                    must=[
                        FieldCondition(
                            key="user_id",
                            match=MatchValue(
                                value=user_id,
                            ),
                        ),
                        FieldCondition(
                            key="session_id",
                            match=MatchValue(
                                value=session_id
                            )
                        )
                    ]
                ),
                k=10,
            )
            logfire.warning(
                f"this is the session id:{session_id} of the search method")

            logfire.info("chunked parse form db sucessfully")
            return [res.page_content for res in results]
        except Exception as error:
            logfire.error(f"exceion occured in vector search{error}")
            raise VectorSearchException(
                f"Error searching for text: {error}") from error

    def qdrent_vector_search(self, user_id, session_id: str, user_input: Union[List[float], float]):
        try:

            respones = self.client.query_points(
                collection_name=secret_manager.qdrent_collection_name,
                query_filter=Filter(
                    must=[
                        FieldCondition(
                            key="user_id",
                            match=MatchValue(
                                value=user_id
                            )
                        ),
                        FieldCondition(
                            key="session_id",
                            match=MatchValue(
                                value=session_id
                            )
                        )
                    ]
                ),
                timeout=60,
                query=user_input,
                with_payload=True
            )

            return [res for res in respones]
        except Exception as error:
            logfire.error(f"Error searching for text in Qdrant: {error}")
            raise VectorSearchException(
                f"Error searching for text in Qdrant: {error}") from error
