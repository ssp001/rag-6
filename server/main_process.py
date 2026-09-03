from app.service import load_the_pdf, text_splitter_service, embedde_the_text, qudrent_vector_upload_service
from uuid import uuid4

"""
def run_process(context, event):
    # Step 1: Load the PDF
    file_path = context
    pdf_response = load_the_pdf(file_path)
    # Step 2: Split the text
    split_text_response = text_splitter_service.spllitte_the_text(
        text=pdf_response.text
    )
    # have to code in modules tomorrow
    # Step 3: Embed the text
    embedding_response = embedde_the_text(split_text_response.chunked_text)

    # Step 4: Upload embeddings to database
    upload_response = qudrent_vector_upload_service.upload_embedding_to_db(
        embeddings=embedding_response.embeddings,
        list_of_text=pdf_response.text,
        user_identity=user_id,
        session_id=str(uuid4())
    )

    return upload_response
"""
