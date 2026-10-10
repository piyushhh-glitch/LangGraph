from langchain_groq import ChatGroq
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()


# 1. Initialize the LLM

llm=ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

# 2. Create a Tool

@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression, such as 25 * 48."""
    # Safe for basic arithmetic only
    import ast
    import operator

    ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in ops:
            return ops[type(node.op)](
                evaluate(node.left),
                evaluate(node.right),
            )
        raise ValueError("Only basic arithmetic is supported")

    return str(evaluate(ast.parse(expression, mode="eval")))


# 3. Create the agent 
agent=create_react_agent(
    model=llm,
    tools=[calculator],
)


# 4. Run the agent
result = agent.invoke({
    "messages": [
        {"role": "user", "content": "What is 25 multiplied by 48?"}
    ]
})

# 5. Print the conversation
for message in result["messages"]:
    print(f"\n{message.type}: {message.content}")
