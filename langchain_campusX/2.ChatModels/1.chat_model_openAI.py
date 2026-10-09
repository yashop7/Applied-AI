from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini" , temperature=0.5 , max_completion_tokens=200)
# You can set the Creativity of the response and the answer limit in Tokens

result = model.invoke("How should a mechanical engineer introduce himself")

print(result.content)