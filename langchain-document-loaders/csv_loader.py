from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(file_path='Social_Network_Ads.csv')

docs = loader.load()


print("Length of Docs",len(docs))
print (docs[0])
print("YASHHAKBFIWEJBFIUEWN")
print(docs[1])