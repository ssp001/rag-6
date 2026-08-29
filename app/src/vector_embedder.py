from sentence_transformers import SentenceTransformer
from app.utils import VectorEmbedderException
from app.config import secret_manager
from numpy import ndarray
import logfire


class VectorEmbedding:
    def __init__(self):
        """
        Initialize the VectorEmbedding class with a SentenceTransformer model.
        """
        self.model = SentenceTransformer(secret_manager.Embedding_model)

    def embed_the_docs(self, text: str) -> list[ndarray]:
        """
        Embed the input text using the SentenceTransformer model.
        """
        try:
            logfire.info("chunkes encoded sucessfully")
            return self.model.encode(text)
        except Exception as error:
            logfire.error(f"exceion occured in vector embedding{error}")
            raise VectorEmbedderException(
                f"Error embedding text: {error}") from error
