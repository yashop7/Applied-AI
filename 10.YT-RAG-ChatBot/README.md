# YT RAG ChatBot

A RAG (Retrieval-Augmented Generation) chatbot that fetches the transcript of a YouTube video and answers questions or summarizes it, using **only** what was said in the video.

Code is present in the Colab notebook:

https://colab.research.google.com/drive/1NwvHC_Qxf5733hZEvytPWxd1UFZxLY6A?usp=sharing

## Tech Stack

- **youtube-transcript-api**: fetches the video transcript
- **LangChain**: text splitting, prompts, runnables and chains
- **OpenAI**: `text-embedding-3-small` for embeddings, `gpt-4o-mini` as the LLM
- **FAISS**: lightweight vector store for similarity search

## How It Works

```
YouTube Video ID
      │
      ▼
 Fetch Transcript ──► Split into Chunks ──► Embeddings ──► FAISS Vector Store
                                                                  │
 User Question ─────────────────────────────► Retriever (top 4) ◄─┘
      │                                              │
      ▼                                              ▼
 Prompt Template (context + question) ──► LLM ──► Answer
```

### Step 1: Indexing

1. **Document Ingestion**: fetch the English transcript with `YouTubeTranscriptApi` and join all snippets into one string. Videos without captions are handled with `TranscriptsDisabled`.
2. **Text Splitting**: `RecursiveCharacterTextSplitter` with `chunk_size=1000`, `chunk_overlap=200`.
3. **Embedding Generation**: each chunk is embedded with `OpenAIEmbeddings(model="text-embedding-3-small")`.
4. **Storing**: the embeddings are stored in a `FAISS` vector store.

### Step 2: Retrieval

The vector store is turned into a retriever with similarity search, returning the **top 4** most relevant chunks for a query.

### Step 3: Augmentation

The retrieved chunks are joined into one context and passed into a prompt template with the question:

```
You are a helpful assistant.
Answer ONLY from the provided transcript context.
If the context is insufficient, just say you don't know.
```

This keeps the model grounded in the video and reduces hallucination.

### Step 4: Generation

`ChatOpenAI(model="gpt-4o-mini", temperature=0.2)` generates the final answer from the augmented prompt.

## Building a Chain

The steps above are then combined into one LangChain pipeline using runnables:

```python
parallel_chain = RunnableParallel({
    'context': retriever | RunnableLambda(format_docs),
    'question': RunnablePassthrough()
})

main_chain = parallel_chain | prompt | llm | StrOutputParser()

main_chain.invoke("Best 5 Points, which are life changing, and most people do that wrong")
```

- `RunnableParallel` runs retrieval and passes the question through at the same time
- `RunnableLambda(format_docs)` joins the retrieved docs into a single context string
- `StrOutputParser` returns the answer as plain text

## Setup

1. Open the Colab notebook above
2. Set your OpenAI API key:
   ```python
   import os
   os.environ["OPENAI_API_KEY"] = "your-api-key"
   ```
3. Install dependencies:
   ```bash
   pip install youtube-transcript-api langchain-community langchain-openai faiss-cpu tiktoken python-dotenv
   ```
4. Change `video_id` to any YouTube video ID (the part after `v=` in the URL) and run all cells

## Example Questions

- "What are the views on multitasking? Is it good? Is it bad?"
- "Best 5 Points, which are life changing, and most people do that wrong"
- "Summarize this video"
