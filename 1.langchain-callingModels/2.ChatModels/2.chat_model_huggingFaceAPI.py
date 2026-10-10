from langchain_huggingface import ChatHuggingFace , HuggingFaceEndpoint

from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation"
)

model = ChatHuggingFace(llm = llm)

question = "Which team won the Fifa 2010 and Why ? who were playing in the Final Round ?"

result = model.invoke(question)

print(result.content)