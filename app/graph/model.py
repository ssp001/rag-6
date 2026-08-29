from app.service import ai_run_query, search_in_db, ai_memory_push, ai_memory_get
from langgraph.graph import StateGraph, START, END
from typing import Union, TypedDict


class InputState(TypedDict):
    """The input state for the graph."""
    user_id: Union[str, None] = None
    session_id: Union[str, None] = None
    ai_respones: Union[str, None] = None
    user_input: Union[str, None] = None
    parsed_memory: Union[str, None] = None
    vector_db_respones: Union[str, None] = None


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

        async for chunk in ai_run_query(
            query=state["user_input"],
            memory_input=state["parsed_memory"],
            parsed_text=state["vector_db_respones"]
        ):
            yield chunk

    except Exception as error:
        raise RuntimeError(str(error))
