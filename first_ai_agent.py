# %%
from dotenv import load_dotenv, find_dotenv
from langchain_core.messages import HumanMessage
load_dotenv(find_dotenv())
# %%
from langchain_groq import ChatGroq
model = ChatGroq(model="llama-3.1-8b-instant")
# %%
from langchain_core.messages import HumanMessage
# %%
from langgraph.graph import START, END, StateGraph, MessagesState

def call_llm(state : MessagesState):
    messages = state["messages"]
    response = model.invoke(messages[-1].content)
    return {"messages": [response]}
#MessageState dispose d'un reducer pré configuré pour concaténer les messages
#start the workflow
builder = StateGraph(MessagesState)
builder.add_node("call_llm", call_llm)
builder.add_edge(START, "call_llm")
builder.add_edge("call_llm", END)
graph = builder.compile()
# %%
###Continuous User Input Processing
def interact_with_agent():
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Ending the conversation.")
            break
        input_message = {"messages": [("human", user_input)]}
        for chunk in graph.stream(input_message, stream_mode="values"):
            chunk["messages"][-1].pretty_print()

# Start interacting with the agent
interact_with_agent()