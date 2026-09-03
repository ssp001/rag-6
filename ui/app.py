import streamlit as st
import requests

API_URL = "http://localhost:8000"

# Initialize session_id
if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "user_id" not in st.session_state:
    st.session_state.user_id = "ssp001"


st.title("RAG Chat")


# -------------------------
# Upload PDF
# -------------------------

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    if st.button("Process PDF"):

        # Save uploaded file locally
        file_path = f"./tmp/{uploaded_file.name}"

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Call backend
        response = requests.post(
            f"{API_URL}/Home/rag_process",
            params={
                "user_id": st.session_state.user_id,
                "file_path": file_path
            }
        )

        if response.status_code == 200:

            data = response.json()

            # IMPORTANT:
            # Save session_id returned by backend
            st.session_state.session_id = data["session_id"]

            st.success(
                f"PDF processed successfully"
            )

            st.write(
                "Session ID:",
                st.session_state.session_id
            )

        else:
            st.error(response.text)


# -------------------------
# Chat
# -------------------------

query = st.chat_input("Ask something about the PDF")

if query:

    if st.session_state.session_id is None:

        st.warning("Please upload and process a PDF first.")

    else:

        response = requests.post(
            f"{API_URL}/Home/respones",
            params={
                "query": query,
                "user_id": st.session_state.user_id,
                "session_id": st.session_state.session_id
            },
            stream=True
        )

        if response.status_code == 200:

            with st.chat_message("assistant"):

                answer = st.write_stream(
                    response.iter_content(
                        chunk_size=None,
                        decode_unicode=True
                    )
                )

        else:
            st.error(response.text)
