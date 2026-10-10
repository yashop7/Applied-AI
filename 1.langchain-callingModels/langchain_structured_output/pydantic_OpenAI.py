
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional, Literal
from pydantic import Field, BaseModel
load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")


# Original the data was in the form of Typed Dictionary
# Yeh bus recommend karta hai, it doesn't enforce, like agar str ki jagah num
# likh diya, no error will be generated
# # schema
# class Review(TypedDict):

#     key_themes: Annotated[list[str], "Write down all the key themes discussed in the review in a list"]
#     summary: Annotated[str, "A brief summary of the review"]
#     sentiment: Annotated[Literal["pos", "neg"], "Return sentiment of the review either negative, positive or neutral"]
#     pros: Annotated[Optional[list[str]], "Write down all the pros inside a list"]
#     cons: Annotated[Optional[list[str]], "Write down all the cons inside a list"]
#     name: Annotated[Optional[str], "Write the name of the reviewer"]


# Now we are defining the schema in the form of Pydantic
# schema
class Review(BaseModel):
#annotated is just for writing extra command, which we have wrote done, LLM shouldn't hallucinate
    key_themes: Annotated[list[str], "Write down all the key themes discussed in the review in a list"]
    summary: Annotated[str, "A brief summary of the review"]
    sentiment: Annotated[Literal["pos", "neg"], "Return sentiment of the review either negative, positive or neutral"]
    pros: Annotated[Optional[list[str]], "Write down all the pros inside a list"]
    cons: Annotated[Optional[list[str]], "Write down all the cons inside a list"]
    name: Annotated[Optional[str], "Write the name of the reviewer"]
    
structured_model = model.with_structured_output(Review)

# we are dropping a review
result = structured_model.invoke("""Things are fine, profuct is amazing by Yash""")
print(result)
# result generated is this : key_themes=['Product quality', 'Customer satisfaction', 'Value for money'] summary='The product is highly praised for its amazing quality and performance, contributing to overall customer satisfaction.' sentiment='pos' pros=['High quality', 'Great performance', 'Good value for money'] cons=None name='Yash'
print(result.summary)


