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

When making use of LLMs to answer questions based on private data, need to provide the relevant documents as context alongside your prompt. This is called Retrieval Augmented Generation (RAG).

We can build a RAG app directly using Gemini API; but also can work through Langchain to make life more easier.

In this demo, we implement the two main components in an RAG-based architecture:

1. Retriever

    Based on the user's query, the retriever retrieves relevant snippets that add context from the document (which is website data here)

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

    USER_AGENT environment variable not set, consider setting it to identify your requests.


## Retriever

Perform the following steps:

- Read and parse the website data using LangChain.
- Create embeddings of the website data.

    Embeddings are numerical representations (vectors) of text. Hence, text with similar meaning will have similar embedding vectors. You'll make use of Gemini's embedding model to create the embedding vectors of the website data.

- Store the embeddings in Chroma's vector store.
    
    Chroma is a vector database. The Chroma vector store helps in the efficient retrieval of similar vectors. Thus, for adding context to the prompt for the LLM, relevant embeddings of the text matching the user's question can be retrieved easily using Chroma.

- Create a Retriever from the Chroma vector store.

    The retriever will be used to pass relevant website embeddings to the LLM along with user queries.

### Read and parse the website data

What is document format from web loader? - [Langchain WebBaseLoader](https://python.langchain.com/v0.2/docs/integrations/document_loaders/web_base/)


```python
loader = WebBaseLoader("https://dreamcloud.artark.ca/build-k8s-cluster-on-wsl2/")
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
#text_content
```


```python
# split text after string
text_content_1 = text_content.split("It is possible to install k8s installation",1)[1]
text_content_1[:200]

```




    ' in one shot using my handy script toolkit.\nFirst of all, download it via git clone, or manually download from github.\n\r\ngit clone git@github.com:robertluwang/hands-on-nativecloud.git\r\ncd ./hands-on-n'




```python
# split text before string
final_text = text_content_1.split("k8s cluster test on WSL2",1)[0]
final_text[-200:]
```




    '-dockerd.sock \r\n\r\necho === $(date) Provisioning - k8s-reset.sh by $(whoami) end\r\n\nFor example,\n\r\nbash k8s-reset.sh\r\n\nthen following k8s-init.sh with eth0 static ip,\n\r\nbash k8s-init.sh 192.168.80.2\r\n\n\n'




```python
# Convert the text to LangChain's `Document` format
docs =  [Document(page_content=final_text, metadata={"source": "local"})]
#docs[0].page_content
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

Create a retriever that can retrieve website data embeddings from the newly created Chroma vector store, it later used to pass embeddings that provide more context to the LLM for answering user's queries.


```python
# Load from disk
vectorstore_disk = Chroma(
                        persist_directory="./chroma_db",       # Directory of db
                        embedding_function=gemini_embeddings   # Embedding model
                   )
retriever = vectorstore_disk.as_retriever(search_kwargs={"k": 1})

print(len(retriever.get_relevant_documents("k8s")))
```

    1


## Generator

The Generator prompts the LLM for an answer when the user asks a question. The retriever you created in the previous stage from the Chroma vector store will be used to pass relevant embeddings from the website data to the LLM to provide more context to the user's query.

You'll perform the following steps in this stage:

1. Chain together the following:
    * A prompt for extracting the relevant embeddings using the retriever.
    * A prompt for answering any question using LangChain.
    * An LLM model from Gemini for prompting.
    
2. Run the created chain with a question as input to prompt the model for an answer.


### Initialize Gemini

We use **gemini-pro** as it supports text summarization. 

Configure the model parameters such as ***temperature*** or ***top_p***,  by passing the appropriate values when initializing the `ChatGoogleGenerativeAI` LLM.


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

We can now query the LLM by passing any question to the `invoke()` function of the stuff documents chain created previously.


```python
from IPython.display import display
from IPython.display import Markdown
import textwrap

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
```


```python
to_markdown(rag_chain.invoke("what is docker-server.sh for? show me source code"))
```




> The docker-server.sh script automates the installation of Docker on Ubuntu systems. It updates the system, installs required packages, adds the Docker repository, installs Docker, adds the current user to the Docker group, disables swap, configures Docker daemon settings, and restarts Docker.
> 
> Here is the source code for the docker-server.sh script:
> 
> ```bash
> # docker-server.sh
> # handy script to install docker on ubuntu 
> # run on k8s cluster node (master/worker)
> # By Robert Wang @github.com/robertluwang
> # Nov 21, 2022
> 
> echo === $(date) Provisioning - docker-server.sh by $(whoami) start
> 
> sudo apt-get update -y
> sudo apt-get install -y ca-certificates curl gnupg lsb-release
> curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
> echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
> sudo apt-get update -y
> sudo apt-get install -y docker-ce docker-ce-cli containerd.io 
> 
> sudo groupadd docker
> sudo usermod -aG docker $USER
> 
> # turn off swap
> sudo swapoff -a
> sudo sed -i '/swap/d' /etc/fstab
> 
> sudo mkdir /etc/docker
> cat <<EOF | sudo tee /etc/docker/daemon.json
> {
>   "exec-opts": ["native.cgroupdriver=systemd"],
>   "log-driver": "json-file",
>   "log-opts": {
>     "max-size": "100m"
>   },
>   "storage-driver": "overlay2"
> }
> EOF
> sudo systemctl enable docker
> sudo systemctl daemon-reload
> sudo systemctl restart docker
> sleep 30 
> sudo systemctl restart docker
> 
> echo === $(date) Provisioning - docker-server.sh by $(whoami) end
> ```



We can see it analyze the code then explain what is doing, also provide completely source code, the only minor issue is output format that is from to_markdown.

## Conclusion

Building a Retrieval-Augmented Generation (RAG) application using Gemini, LangChain, and Chroma demonstrates the powerful capabilities of combining generative AI models with efficient data retrieval and embedding storage. This approach leverages the strengths of each component: Gemini's advanced generative models, LangChain's integration framework, and Chroma's efficient embedding database. 

By following the steps outlined, you can create an application that answers questions with high accuracy by providing relevant context from a specific data source. This not only enhances the quality of the responses but also ensures that the information provided is contextually relevant and precise.

The integration of these tools simplifies the development process, making it easier to implement complex AI-driven solutions. Whether you are working on a chatbot, a customer support system, or any application that requires context-aware responses, this demo provides a solid foundation for building effective RAG applications.


```python

```
