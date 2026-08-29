from app.service import load_the_pdf, text_splitter_service, embedde_the_text, qudrent_vector_upload_service

import logfire
import requests


def run_process(user_id, file_path: str):
    # Step 1: Load the PDF

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
        user_identity=user_id
    )

    return upload_response


if __name__ == "__main__":
    # Example usage of the test_qudrent function
    test_query = "Sample query for testing"
    test_session_id = "cfa40a10-f192-44c2-8359-86387c4826ae"
    test_user_id = "723908uowi"

    result = run_process(user_id=test_user_id, file_path="C:/Users/shova/Documents/designing-data-intensive-applications-the-big-ideas-behind-reliable-scalable-and-maintainable-systems-1nbsped-9781449373320-1449373321_compress.pdf")
    print(result)
