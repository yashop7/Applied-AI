from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
load_dotenv()

documents = [
    "Virat Kohli is an Indian cricketer known for his aggressive batting and leadership.",
    "MS Dhoni is a former Indian captain famous for his calm demeanor and finishing skills.",
    "Sachin Tendulkar, also known as the 'God of Cricket', holds many batting records.",
    "Rohit Sharma is known for his elegant batting and record-breaking double centuries.",
    "Jasprit Bumrah is an Indian fast bowler known for his unorthodox action and yorkers."
]

embeddings = OpenAIEmbeddings(model = "text-embedding-3-large")


query = "Tell me about Virat Kohli"

doc_embeddings = embeddings.embed_documents(documents)
query_embeddings = embeddings.embed_query(query)

scores = cosine_similarity([query_embeddings] , doc_embeddings)[0]

# index, score = sorted()

index , score = sorted(list(enumerate(scores)),key = lambda x:x[1])[-1] # sorting on the Basis of 2nd Item, that's how we wrote the Lambda thing
# -1 for the Biggest

print("Query asked", query)
print("Relevant result",documents[index])
print("Similarity Score",score)

#Retrival is process we find the Similarity score of Query and Documents, and retrieve the relevant Documents