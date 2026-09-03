from fastapi.responses import StreamingResponse
from app.graph import ai_respones

"""
async def chat(context, event):

    state = {
        "user_id": user_id,
        "session_id": session_id,
        "user_input": query
    }

    return StreamingResponse(
        content=ai_respones(state),
        media_type="text/plain"
    )
"""
