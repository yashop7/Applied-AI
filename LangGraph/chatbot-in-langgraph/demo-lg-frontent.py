import streamlit as st

# from lg_backend import chatbot
from langchain_core.messages import HumanMessage
# Because any message I will pass, will be wrapped in the Human Message


CONFIG = {'configurable' : {'thread_id' : "thread-1"}}


with st.chat_message('user'):
    st.text('Hi')
with st.chat_message("ai"):
    st.text('How can I help you')
with st.chat_message('assistant'):
    st.text('How can I help you')
with st.chat_message('human'):
    st.text('YO')
    
user_input = st.chat_input("Type here ...")

if user_input:
    with st.chat_message('human'):
        st.text(user_input)
    


