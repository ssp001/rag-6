from langchain_community.document_loaders import PyPDFLoader
from app.utils import PdfLoderException
from typing import List
import logfire


class PdfLoder:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_pdf(self) -> List[str]:
        try:
            list_of_text = []
            loader = PyPDFLoader(file_path=self.file_path)
            document = loader.load()
            for i in document:
                text = i.page_content
                list_of_text.append(text)
            logfire.info("document loded sucessfully")
            return list_of_text
        except Exception as error:
            logfire.error(f"Error loading PDF: {error}")
            raise PdfLoderException(f"Error loading PDF: {error}")
