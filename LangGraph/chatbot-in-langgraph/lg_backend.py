from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from dotenv import load_dotenv

load_dotenv()

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]
    

llm = ChatOpenAI()

# Checkpointer
checkpointer = InMemorySaver()


def chat_node(state : ChatState):
    # now we will add the chats
    messages = state['messages']
    output = llm.invoke(messages)
    # Now we get the Output, we will return it
    return {'messages' : [output]}


graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)
graph.add_edge(START, chat_node)
graph.add_edge(chat_node, END)

chatbot = graph.compile(checkpointer=checkpointer)
