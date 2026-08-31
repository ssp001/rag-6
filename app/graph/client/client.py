from app.config import InputState
from app.service import ai_run_query, search_in_db, ai_memory_search, ai_memory_push


def vector_db_search(state: InputState):
    try:
        db_respones = search_in_db(
            query=state["user_input"],
            session_id=state["session_id"],
            user_id=state["user_id"]
        )
        state["vector_db_respones"] = db_respones
        return state
    except Exception as error:
        raise RuntimeError(str(error))


def search_memory(state: InputState):
    try:
        search_respones = ai_memory_search(
            user_chat=state["user_input"],
            user_id=state["user_id"],
            session_id=state["memory_session_id"]
        )
        state["parsed_memory"] = search_respones
        return state
    except Exception as error:
        raise RuntimeError(str(error))


def push_to_memory(state: InputState):
    try:
        respones = ai_memory_push(
            session_id=state["session_id"],
            user_chat=state["user_input"],
            user_id=state["user_id"]
        )
        state["memory_session_id"] = respones
        return state
    except Exception as error:
        raise RuntimeError(str(error))


async def ai_run(state: InputState):
    try:
        respones = ""
        memory_input = state.get("parsed_memory", [])
        async for chunk in ai_run_query(
            query=state["user_input"],
            memory_input=memory_input,
            parsed_text=state["vector_db_respones"]
        ):
            respones += chunk
            state["ai_respones"] = respones
        return {
            "ai_respones": respones
        }

    except Exception as error:
        raise RuntimeError(str(error))
