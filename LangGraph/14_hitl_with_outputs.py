# ===== Cell 1 =====
from typing import Annotated

from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, AIMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage


# ===== Cell 2 =====
load_dotenv()

# Output:
# True


# ===== Cell 3 =====
llm = ChatOpenAI(model="gpt-4.1-mini")


# ===== Cell 4 =====
from langgraph.graph.message import add_messages

class ChatState(TypedDict):

    messages: Annotated[list[BaseMessage], add_messages]


# ===== Cell 5 =====
def chat_node(state: ChatState):

    decision = interrupt({
        "type": "approval",
        "reason": "Model is about to answer a user question.",
        "question": state["messages"][-1].content,
        "instruction": "Approve this question? yes/no"
    })
    
    if decision["approved"] == 'no':
        return {"messages": [AIMessage(content="Not approved.")]}

    else:
        response = llm.invoke(state["messages"])
        return {"messages": [response]}


# ===== Cell 6 =====
# 3. Build the graph: START -> chat -> END
builder = StateGraph(ChatState)

builder.add_node("chat", chat_node)

builder.add_edge(START, "chat")
builder.add_edge("chat", END)

# Checkpointer is required for interrupts
checkpointer = MemorySaver()

# Compile the app
app = builder.compile(checkpointer=checkpointer)


# ===== Cell 7 =====
app

# Output:
# <langgraph.graph.state.CompiledStateGraph object at 0x10ef47e50>


# ===== Cell 8 =====
# Create a new thread id for this conversation
config = {"configurable": {"thread_id": '1234'}}

# ---- STEP 1: user asks a question ----
initial_input = {
    "messages": [
        ("user", "Explain gradient descent in very simple terms.")
    ]
}

# Invoke the graph for the first time
result = app.invoke(initial_input, config=config)


# ===== Cell 9 =====
result

# Output:
# {'messages': [HumanMessage(content='Explain gradient descent in very simple terms.', additional_kwargs={}, response_metadata={}, id='d7bb9cc8-e132-4afe-a673-33d279309b83'),
#   AIMessage(content='Not approved.', additional_kwargs={}, response_metadata={}, id='5b53bc94-8113-4b8e-8344-d9ebcf26d8a1'),
#   HumanMessage(content='Explain gradient descent in very simple terms.', additional_kwargs={}, response_metadata={}, id='8b0dd45c-af99-497b-b665-9b25f0652427')],
#  '__interrupt__': [Interrupt(value={'type': 'approval', 'reason': 'Model is about to answer a user question.', 'question': 'Explain gradient descent in very simple terms.', 'instruction': 'Approve this question? yes/no'}, id='8f970c37f92bf4a907ec29209ca75371')]}


# ===== Cell 10 =====
message = result['__interrupt__'][0].value
message

# Output:
# {'type': 'approval',
#  'reason': 'Model is about to answer a user question.',
#  'question': 'Explain gradient descent in very simple terms.',
#  'instruction': 'Approve this question? yes/no'}


# ===== Cell 11 =====
user_input = input(f"\nBackend message - {message} \n Approve this question? (y/n): ")


# ===== Cell 12 =====
# Resume the graph with the approval decision
final_result = app.invoke(
    Command(resume={"approved": user_input}),
    config=config,
)


# ===== Cell 13 =====
print(final_result["messages"][-1].content)

# Output:
# {'messages': [HumanMessage(content='Explain gradient descent in very simple terms.', additional_kwargs={}, response_metadata={}, id='d7bb9cc8-e132-4afe-a673-33d279309b83'), AIMessage(content='Not approved.', additional_kwargs={}, response_metadata={}, id='5b53bc94-8113-4b8e-8344-d9ebcf26d8a1'), HumanMessage(content='Explain gradient descent in very simple terms.', additional_kwargs={}, response_metadata={}, id='8b0dd45c-af99-497b-b665-9b25f0652427'), AIMessage(content='Sure! Imagine you\'re standing on a hill, and your goal is to reach the lowest point in the valley. However, it\'s foggy, so you can\'t see very far. To get down, you take small steps going downhill, always moving in the direction where the slope goes down the most. By repeating this—taking small steps downhill—you eventually reach the bottom.\n\nGradient descent is like that, but for finding the best solution in math or machine learning. Instead of a hill, you have a "function" to minimize (like an error or cost), and gradient descent helps you find the lowest value by moving step-by-step in the direction that decreases the function the most.', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 135, 'prompt_tokens': 34, 'total_tokens': 169, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4.1-mini-2025-04-14', 'system_fingerprint': 'fp_7abc656409', 'id': 'chatcmpl-ClhBeWsooklp4onV99tmsEVM90jIz', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None}, id='run--03cb1826-6715-4ecd-a851-cb0135e50896-0', usage_metadata={'input_tokens': 34, 'output_tokens': 135, 'total_tokens': 169, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})]}


# ===== Cell 14 =====


