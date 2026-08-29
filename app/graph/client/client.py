from app.config import InputState
from app.service import ai_run_query, search_in_db, ai_memory_push, ai_memory_get


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
        search_respones = ai_memory_get(
            user_chat=state["user_input"],
            user_id=state["user_id"],
            session_id=state["session_id"]
        )
        state["parsed_memory"] = search_respones
        return state
    except Exception as error:
        raise RuntimeError(str(error))


def push_to_memory(state: InputState):
    try:
        ai_memory_push(
            ai_respoones=state["ai_respones"],
            session_id=state["session_id"],
            user_chat=state["user_input"],
            user_id=state["user_id"]
        )
        return state
    except Exception as error:
        raise RuntimeError(str(error))


async def ai_run(state: InputState):
    try:
        respones = ""
        async for chunk in ai_run_query(
            query=state["user_input"],
            memory_input=state["parsed_memory"],
            parsed_text=state["vector_db_respones"]
        ):
            respones += chunk
            state["ai_respones"] = respones
            return respones

    except Exception as error:
        raise RuntimeError(str(error))


def router_node(state: InputState):
    try:
        search_respones = ai_memory_get(
            user_chat=state["user_input"],
            user_id=state["user_id"],
            session_id=state["session_id"]
        )
        state["memory_condition"] = search_respones
        return state
    except Exception as error:
        raise RuntimeError(str(error))


def memory_router(state: InputState):
    try:
        if state["memory_condition"] is None:
            return "push_memory"

        elif state["memory_condition"]:
            return "search_memory"

        else:
            return "push_memory"
    except Exception as error:
        raise RuntimeError(str(error))
