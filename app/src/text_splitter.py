from langchain_text_splitters.character import CharacterTextSplitter
from typing import List
import logfire
from app.utils import TextSplitterException


class TextSplitter:
    def __init__(self):
        self.text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len
        )

    def split_text(self, text: str) -> List[str]:
        try:
            logfire.info("text chunked suscessfully")
            return self.text_splitter.split_text(text)
        except Exception as error:
            logfire.error(f"TextSplitterExceion error occured:{error}")
            raise TextSplitterException(
                f"Error splitting text: {error}") from error
