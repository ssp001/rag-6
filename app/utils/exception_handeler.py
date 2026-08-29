class PdfLoderException(Exception):
    """
    Custom exception class for handling errors related to PDF loading.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class QuadrentVectorException(Exception):
    """
    Custom exception class for handling errors related to Qdrant vector operations.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class TextSplitterException(Exception):
    """
    Custom exception class for handling errors related to text splitting operations.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class VectorEmbedderException(Exception):
    """
    Custom exception class for handling errors related to vector embedding operations.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class VectorSearchException(Exception):
    """
    Custom exception class for handling errors related to vector search operations.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class AiResponesException(Exception):
    """
    Custom exception class for handling errors related to AI response operations.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class AiMemoryException(Exception):
    """
    Custom exception class for handling errors related to AI memory response operations.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
