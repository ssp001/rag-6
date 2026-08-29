from fastapi import FastAPI
from app.graph import ai_respones
from app.config import secret_manager
from fastapi.responses import StreamingResponse
from uuid import uuid4
from app.service import (
    load_the_pdf,
    text_splitter_service,
    embedde_the_text,
    qudrent_vector_delete_service,
    qudrent_vector_upload_service,
)
from app.graph import model
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
async def chat(query: str, user_id: str, session_id: str):

    state = {
        "user_id": user_id,
        "session_id": session_id,
        "user_input": query
    }

    return StreamingResponse(
        content=ai_respones(state),
        media_type="text/plain"
    )
