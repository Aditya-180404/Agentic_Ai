from fastapi import FastAPI
from pydantic import BaseModel
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY")
)

response = llm.invoke("hello")
print(response.content)

class State(TypedDict):
    messages:Annotated[list,add_messages]


def chatbot_node (state:State):
    responce=llm.invoke(state["messages"])
    return {"messages":[responce]}

graph_builder=StateGraph(State)
graph_builder.add_node("chatbot",chatbot_node)
                       
graph_builder.add_edge(START,"chatbot")

graph_builder.add_edge("chatbot",END)

graph=graph_builder.compile()

response=graph.invoke({"messages":"today weather"})

print(response["messages"][-1].content)