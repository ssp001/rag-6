from langgraph.graph import StateGraph, START, END
from app.graph.client import vector_db_search, search_memory, ai_run, push_to_memory, InputState


graph = StateGraph(InputState)

graph.add_node("vector_db", vector_db_search)
graph.add_node("search_memory", search_memory)
graph.add_node("push_memory", push_to_memory)
graph.add_node("ai_run", ai_run)

graph.add_edge(START, "vector_db")
graph.add_edge("vector_db", "push_memory")
graph.add_edge("push_memory", "search_memory")
graph.add_edge("search_memory", "ai_run")
graph.add_edge("ai_run", END)

model = graph.compile()


async def ai_respones(state: InputState):
    async for chunk, metadata in model.astream(
        state,
        stream_mode="messages"
    ):

        yield chunk.content.encode("utf-8")
