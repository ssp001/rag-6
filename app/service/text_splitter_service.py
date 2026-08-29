from app.utils import TextSplitterRespones, json_dump, json_loader
from app.src import TextSplitter
from app.utils import TextSplitterException
from .pdf_loder_service import load_the_pdf
from pyresilience import resilient, TimeoutConfig, RetryConfig
from typing import List


@resilient(
    timeout=TimeoutConfig(
        seconds=60,
    ),
    retry=RetryConfig(
        max_attempts=3,
        delay=10
    )
)
def spllitte_the_text(text: load_the_pdf) -> TextSplitterRespones:
    try:
        text_splitter_client = TextSplitter()
        for line_of_text in text:
            chnked_text = text_splitter_client.split_text(text=line_of_text)
            model = TextSplitterRespones(
                chunked_text=chnked_text
            )
        return model
    except TextSplitterException as error:
        raise RuntimeError(f"Error chunking text: {error}")
