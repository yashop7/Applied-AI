from langchain_huggingface import ChatHuggingFace , HuggingFaceEndpoint

from dotenv import load_dotenv

import os

load_dotenv()

os.environ['HF_HOME'] = 'D:/huggingface_cache'

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    #we can also set the parameters
    max_new_tokens=200, # Setting the Max Tokens
    temperature=0.3
    
)

model = ChatHuggingFace(llm = llm)

question = "Which team won the Fifa 2010 and Why ? who were playing in the Final Round ?"

result = model.invoke(question)

print(result.content)