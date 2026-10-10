from langchain_openai import OpenAI
from dotenv import load_dotenv
 
load_dotenv()

llm = OpenAI(model = "gpt-3.5-turbo-instruct")

result = llm.invoke("I love you in spanish")

print(result)

# DON'T USE THIS CODE