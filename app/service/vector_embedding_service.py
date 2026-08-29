from app.src import VectorEmbedding
from app.utils import VectorEmbedderException
from .text_splitter_service import spllitte_the_text
from typing import List
from app.utils import json_loader, json_dump, VectorEmbeddingRespones
from pyresilience import resilient, TimeoutConfig, RetryConfig


@resilient(
    timeout=TimeoutConfig(
        seconds=60,
    ),
    retry=RetryConfig(
        max_attempts=3,
        delay=10
    )
)
def embedde_the_text(list_of_text: spllitte_the_text) -> VectorEmbeddingRespones:
    """
    Function to split the text into chunks and build embeddings for each chunk.
    """
    try:
        text_splitter_client = VectorEmbedding()
        embedded_text = text_splitter_client.embed_the_docs(
            text=list_of_text
        )
        model = VectorEmbeddingRespones(
            embeddings=embedded_text
        )
        return model
    except VectorEmbedderException as error:
        raise RuntimeError(
            f"Error in buliding embedding's of the text: {error}")
