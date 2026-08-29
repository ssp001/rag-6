import streamlit as st
import requests
import json

# --- CONFIGURATION ---
FASTAPI_BASE_URL = "http://127.0.0.1:8000"  # Adjust to your Uvicorn host/port

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="wide")

# --- INITIALIZE SESSION STATE ---
# This keeps track of history and files across user clicks without wiping data
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processed_files" not in st.session_state:
    st.session_state.processed_files = []
if "user_id" not in st.session_state:
    # Simulated authenticated session ID
    st.session_state.user_id = "user_default_123"

# --- SIDEBAR: KNOWLEDGE MANAGEMENT ---
with st.sidebar:
    st.title("📂 Session Assets")
    st.subheader("Ingest New Documents")

    # 1. Inputs required by your /Home/rag_process endpoint
    file_path_input = st.text_input(
        "Absolute Server File Path:",
        placeholder="C:/docs/sample.pdf"
    )

    if st.button("🚀 Process & Embed PDF", use_container_width=True):
        if file_path_input:
            with st.spinner("Processing document layout and uploading vectors..."):
                try:
                    # Matches your endpoint signature: /Home/rag_process?user_id=...&file_path=...
                    params = {
                        "user_id": st.session_state.user_id,
                        "file_path": file_path_input
                    }
                    response = requests.post(
                        f"{FASTAPI_BASE_URL}/Home/rag_process", params=params)

                    if response.status_code == 200:
                        st.success("Document ingestion successful!")
                        st.session_state.processed_files.append(
                            file_path_input)
                    else:
                        st.error(
                            f"Error ({response.status_code}): {response.text}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {e}")
        else:
            st.warning("Please supply a valid absolute file path string.")

    st.divider()

    # 2. Vector Point Deletion Segment
    st.subheader("Danger Zone")
    session_id_to_delete = st.text_input(
        "Target Session ID to Wipe:", placeholder="session_abc123")

    if st.button("🗑️ Clear Vector Points", type="primary", use_container_width=True):
        if session_id_to_delete:
            with st.spinner("Clearing remote Qdrant collections..."):
                try:
                    # Matches your endpoint: /Home/delete?session_id=...&user_id=...
                    params = {
                        "session_id": session_id_to_delete,
                        "user_id": st.session_state.user_id
                    }
                    del_response = requests.delete(
                        f"{FASTAPI_BASE_URL}/Home/delete", params=params)
                    if del_response.status_code == 200:
                        st.success("Session embedding data destroyed.")
                    else:
                        st.error(
                            f"Delete operation dropped: {del_response.text}")
                except Exception as e:
                    st.error(f"Network error during deletion: {e}")
        else:
            st.warning("Provide a Session ID to trigger vector removal.")

# --- MAIN INTERFACE: STREAMING CHAT INTERFACE ---
st.title("💬 RAG Conversational Engine")
st.caption(
    "Interact with context extracted directly from your structural vector stores.")

# Render existing conversation timeline from session memory
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Captures user query from input line
if user_query := st.chat_input("Ask a question about your embedded documents..."):

    # Display the user's message immediately
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Display empty container box for assistant response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_text_accumulator = ""

        try:
            # Matches your endpoint: /Home/respones?query=...
            # We configure stream=True to process chunks over the live socket connection
            params = {
                "query": user_query,
                "session_id": session_id_to_delete,
                "user_id": "user_82639"
            }

            with requests.post(f"{FASTAPI_BASE_URL}/Home/respones", params=params, stream=True) as response:
                if response.status_code == 200:
                    # Iterate through incoming data fragments as they arrive
                    for chunk in response.iter_content(chunk_size=128, decode_unicode=True):
                        if chunk:
                            full_text_accumulator += chunk
                            # Update UI widget dynamically on-the-fly
                            response_placeholder.markdown(
                                full_text_accumulator + "▌")

                    # Final clean display without the cursor indicator
                    response_placeholder.markdown(full_text_accumulator)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": full_text_accumulator})
                else:
                    error_msg = f"Backend failure encountered. (Code: {response.status_code})"
                    response_placeholder.markdown(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg})

        except Exception as conn_err:
            ex_msg = f"Could not stream response chunk lines from model router: {conn_err}"
            response_placeholder.markdown(ex_msg)
            st.session_state.messages.append(
                {"role": "assistant", "content": ex_msg})
