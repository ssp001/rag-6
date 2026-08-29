from fastapi import FastAPI
from app.config import secret_manager
from fastapi.responses import StreamingResponse
from uuid import uuid4
from app.service import (
    load_the_pdf,
    text_splitter_service,
    embedde_the_text,
    ai_run_query,
    qudrent_vector_delete_service,
    qudrent_vector_upload_service,
    search_in_db,
    qudrent_query_point_search
)
import logfire
app = FastAPI(title="rag_endpoint")
logfire.configure(
    service_name="rag-6",
    api_key=secret_manager.Logfier_key
)


@app.get("/Home")
def Home_page():
    return {"message": "Welcome to the RAG API!"}


@app.post("/Home/rag_process")
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
        user_identity=user_id,
        session_id=str(uuid4())
    )

    return upload_response


@app.delete("/Home/delete")
def delete_vector_points(session_id: str, user_id: str):
    delete_response = qudrent_vector_delete_service.delete_embedding_from_db(
        user_identity=user_id,
        session_indentity=session_id
    )

    return delete_response


@app.post("/Home/respones")
async def ai_respones(user_id: str, query: str, session_id: str):
    search_response = search_in_db(
        user_id=user_id,
        query=query,
        session_id=session_id
    )
    return StreamingResponse(
        ai_run_query(query=query, parsed_text=search_response),
        media_type="text/plain"
    )


@app.post("/Home/test_qudrent")
def test_qudrent(query: str, session_id: str, user_id: str):
    try:
        response = qudrent_query_point_search(
            user_input=query,
            user_id=user_id,
            session_id=session_id
        )
        return {"message": "Qdrant connection successful!", "response": response}
    except Exception as error:
        logfire.error(f"Error testing Qdrant connection: {error}")
        return {"message": f"Error testing Qdrant connection: {error}"}
