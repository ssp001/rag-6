from app.src import PdfLoder
from app.utils import PdfLoderException
from pyresilience import resilient, TimeoutConfig, RetryConfig
from app.utils import json_dump, PdfLoderRespoens
from app.utils import PdfLoderRespoens


@resilient(
    timeout=TimeoutConfig(
        seconds=60,
    ),
    retry=RetryConfig(
        max_attempts=3,
        delay=10
    )
)
def load_the_pdf(file_path: str) -> PdfLoderRespoens:
    try:
        pdf_loder_client = PdfLoder(
            file_path=file_path
        )
        text_data = pdf_loder_client.load_pdf()
        model = PdfLoderRespoens(
            text=text_data
        )
        return model
    except PdfLoderException as error:
        raise RuntimeError(f"Error loading PDF: {error}")
