# Build RAG App using Gemini+LangChain+Chroma

## Overview

[Gemini](https://ai.google.dev/models/gemini) - family of generative AI models used to generate content and solve problems; used to handle both text and images as input.

[LangChain](https://www.langchain.com/) - data framework to integrate with Large Language Models (LLM) like Gemini easier for applications.

[Chroma](https://docs.trychroma.com/) - open-source embedding database focused on simplicity and productivity; used to store embeddings and metadata, embed documents and queries, and search the embeddings quickly.

Here is demo how to create a RAG application that answers questions using data from a website using Gemini, LangChain, and Chroma.

## Installation


```python
!pip install --quiet langchain langchain_community
!pip install --quiet langchain-google-genai
!pip install --quiet chromadb
```

## Setup API key

Place below line to .env under current folder, 

GOOGLE_API_KEY=xxx


```python
import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
```

## RAG

when making use of LLMs to answer questions based on private data, need to provide the relevant documents as context alongside your prompt. This is called Retrieval Augmented Generation (RAG).

You can build a RAG app directly using Gemini API; also can work through Langchain.

In this demo, will implement the two main components in an RAG-based architecture:

1. Retriever

    Based on the user's query, the retriever retrieves relevant snippets that add context from the document which is website data.

2. Generator

    The relevant snippets from the website data are passed to the LLM along with the user's query to generate accurate answers.

## Import the required libraries


```python
from langchain import PromptTemplate
from langchain import hub
from langchain.docstore.document import Document
from langchain.document_loaders import WebBaseLoader
from langchain.schema import StrOutputParser
from langchain.schema.prompt_template import format_document
from langchain.schema.runnable import RunnablePassthrough
from langchain.vectorstores import Chroma
```

## Retriever

perform the following steps:

- Read and parse the website data using LangChain.
- Create embeddings of the website data.

    Embeddings are numerical representations (vectors) of text. Hence, text with similar meaning will have similar embedding vectors. You'll make use of Gemini's embedding model to create the embedding vectors of the website data.

- Store the embeddings in Chroma's vector store.
    
    Chroma is a vector database. The Chroma vector store helps in the efficient retrieval of similar vectors. Thus, for adding context to the prompt for the LLM, relevant embeddings of the text matching the user's question can be retrieved easily using Chroma.

- Create a Retriever from the Chroma vector store.

    The retriever will be used to pass relevant website embeddings to the LLM along with user queries.

### Read and parse the website data

what is document format from web loader? - [Langchain WebBaseLoader](https://python.langchain.com/v0.2/docs/integrations/document_loaders/web_base/)


```python
loader = WebBaseLoader("https://blog.google/technology/ai/google-gemini-ai/")
docs = loader.load()
#docs[0]
#docs[0].metadata ## dict
#docs[0].page_content ## string
```

If you only want to select a specific portion of the website data to add context to the prompt, you can use regex, text slicing, or text splitting.

We use split function to extract the required portion of the text. The extracted text should be converted back to LangChain's `Document` format.
> `docs =  [Document(page_content=final_text, metadata={"source": "local"})]`


```python
# Extract the text from the website data document
text_content = docs[0].page_content
text_content
```


```python
# The text content between the substrings "code, audio, image and video." to
# "Cloud TPU v5p" is relevant for this tutorial. You can use Python's `split()`
# to select the required content.
text_content_1 = text_content.split("code, audio, image and video.",1)[1]
text_content_1
final_text = text_content_1.split("Cloud TPU v5p",1)[0]
final_text

```


```python
# Convert the text to LangChain's `Document` format
docs =  [Document(page_content=final_text, metadata={"source": "local"})]
docs[0].page_content
```

### Initialize Gemini's embedding model

**embedding-001** supports creating text embeddings.


```python
from langchain_google_genai import GoogleGenerativeAIEmbeddings

gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
```

### Store the data using Chroma



```python
# Save to disk
vectorstore = Chroma.from_documents(
                     documents=docs,                 # Data
                     embedding=gemini_embeddings,    # Embedding model
                     persist_directory="./chroma_db" # Directory to save data
                     )
```

### Create a retriever using Chroma

create a retriever that can retrieve website data embeddings from the newly created Chroma vector store. This retriever can be later used to pass embeddings that provide more context to the LLM for answering user's queries.


```python
# Load from disk
vectorstore_disk = Chroma(
                        persist_directory="./chroma_db",       # Directory of db
                        embedding_function=gemini_embeddings   # Embedding model
                   )
retriever = vectorstore_disk.as_retriever(search_kwargs={"k": 1})

print(len(retriever.get_relevant_documents("MMLU")))
```

## Generator

The Generator prompts the LLM for an answer when the user asks a question. The retriever you created in the previous stage from the Chroma vector store will be used to pass relevant embeddings from the website data to the LLM to provide more context to the user's query.

perform the following steps:

1. Chain together the following:
    * A prompt for extracting the relevant embeddings using the retriever.
    * A prompt for answering any question using LangChain.
    * An LLM model from Gemini for prompting.
    
2. Run the created chain with a question as input to prompt the model for an answer.


### Initialize Gemini

We use **gemini-pro** as it supports text summarization. 

configure the model parameters such as ***temperature*** or ***top_p***,  by passing the appropriate values when initializing the `ChatGoogleGenerativeAI` LLM. 


```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-pro",
                 temperature=0.7, top_p=0.85)
```

### Create prompt templates

Use LangChain's [PromptTemplate](https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/) to generate prompts to the LLM for answering questions.


```python
# Prompt template to query Gemini
llm_prompt_template = """You are an assistant for question-answering tasks.
Use the following context to answer the question.
If you don't know the answer, just say that you don't know.
Use five sentences maximum and keep the answer concise.\n
Question: {question} \nContext: {context} \nAnswer:"""

llm_prompt = PromptTemplate.from_template(llm_prompt_template)

print(llm_prompt)
```

    input_variables=['context', 'question'] template="You are an assistant for question-answering tasks.\nUse the following context to answer the question.\nIf you don't know the answer, just say that you don't know.\nUse five sentences maximum and keep the answer concise.\n\nQuestion: {question} \nContext: {context} \nAnswer:"


### Create a stuff documents chain

LangChain provides [Chains](https://python.langchain.com/docs/modules/chains/) for chaining together LLMs with each other or other components for complex applications. 

The stuff documents chain for this application retrieves the relevant website data and passes it as the context to an LLM prompt along with the input question.


```python
# Combine data from documents to readable string format.
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | llm_prompt
    | llm
    | StrOutputParser()
)
```

### Prompt the model

You can now query the LLM by passing any question to the `invoke()` function of the stuff documents chain you created previously.


```python
rag_chain.invoke("What is Gemini?")
```




    "Gemini is Google's largest and most capable AI model. It is the first model to outperform human experts on MMLU (massive multitask language understanding). Gemini is natively multimodal, pre-trained from the start on different modalities. It can understand and reason about all kinds of inputs from the ground up. Gemini is also our most flexible model yet — able to efficiently run on everything from data centers to mobile devices."



## Conclusion

This article demos a LLM application that answers questions using data from a website with the help of Gemini, LangChain, and Chroma.


```python

```
