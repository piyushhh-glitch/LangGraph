from typing import TypedDict
from langgraph.graph import StateGraph , START, END

class State(TypedDict):
    message: str


def greet(state=State):
    return {"message":"hello from langgraph"}

graph=StateGraph(State)

graph.add_node("greet",greet)


graph.add_edge(START,"greet")
graph.add_edge("greet",END)


app=graph.compile()

result=app.invoke({"message":"hello"})

print(result)