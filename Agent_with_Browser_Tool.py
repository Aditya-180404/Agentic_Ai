from fastapi import FastAPI
from pydantic import BaseModel
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()

from langchain_tavily import TavilySearch

llm=ChatGroq(model="openai/gpt-oss-20b",api_key=os.getenv("GROQ_API_KEY"))
llm.invoke("give me the yesterday news").content
tool=TavilySearch(max_results=2,api_key=os.getenv("TAVILY_API_KEY"))
def multiply(a:int,b:int)->int:
    """
    Multiply two intigers.Use only if asked to calculate a product

    Args:
        a (int):First int
        b (int):Second int
   
    Returns:
        int:output int
    
    """
    return a*b
tools=[tool,multiply]
llm_with_tools=llm.bind_tools(tools)
class State(TypedDict):
    messages:Annotated[list,add_messages]
def chatbot(state:State):
    return {"messages":[llm.invoke(State['messages'])]}
from langgraph.prebuilt import ToolNode,tools_condition

def tool_cailing_llm(state:State):
    return {"messages":[llm_with_tools.invoke(state["messages"])]}


graph_builder=StateGraph(State)

graph_builder.add_node("chatbot",tool_cailing_llm)
graph_builder.add_node("tool_node",ToolNode(tools))

graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
    {
        "tools":"tool_node",
        "end":END
    }
)
graph_builder.add_edge("chatbot",END)

graph=graph_builder.compile()

from IPython.display import Image,display
display(Image(graph.get_graph().draw_mermaid_png()))
response=graph.invoke({"messages":"give me recent ai news made yesterday"})
for m in response["messages"]:
    m.pretty_print()
from langgraph.prebuilt import ToolNode,tools_condition

def tool_cailing_llm(state:State):
    return {"messages":[llm_with_tools.invoke(state["messages"])]}


graph_builder=StateGraph(State)

graph_builder.add_node("chatbot",tool_cailing_llm)
graph_builder.add_node("tool_node",ToolNode(tools))

graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
    {
        "tools":"tool_node",
        "__end__":END
    }
)
graph_builder.add_edge("tool_node","chatbot")
graph_builder.add_edge("chatbot",END)

graph=graph_builder.compile()

from IPython.display import Image,display
display(Image(graph.get_graph().draw_mermaid_png()))
response=graph.invoke({"messages":"give me recent ai news made yesterday"})
for m in response["messages"]:
    m.pretty_print()
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.checkpoint.memory import MemorySaver

memory=MemorySaver()


def tool_cailing_llm(state:State):
    return {"messages":[llm_with_tools.invoke(state["messages"])]}


graph_builder=StateGraph(State)

graph_builder.add_node("chatbot",tool_cailing_llm)
graph_builder.add_node("tool_node",ToolNode(tools))

graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
    {
        "tools":"tool_node",
        "__end__":END
    }
)
graph_builder.add_edge("tool_node","chatbot")
graph_builder.add_edge("chatbot",END)

graph=graph_builder.compile(checkpointer=memory)

config={"configurable" : {"thread_id":"1"}}
response=graph.invoke({"messages":"my name is adi"},config=config)
response["messages"][-1].content
response=graph.invoke({"messages":"what is my name"},config=config)
response["messages"][-1].content
config2={"configurable" : {"thread_id":"2"}}
response=graph.invoke({"messages":"what is my name"},config=config2)
response["messages"][-1].content
