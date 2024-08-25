# Unleash the Power of RAG - Building Intelligent Apps with Chroma and Gemini Pro

## Introduction

The field of Generative AI (GenAI) is rapidly evolving, offering exciting possibilities for applications that interact with and understand human language. One promising approach is Retriever-Augmented Generation (RAG), which combines information retrieval with powerful language models. This blog delves into building a RAG application using Chroma, a vector database, and Gemini Pro, a state-of-the-art large language model from Google.

**Chroma: The Key to Efficient Information Retrieval**

Chroma serves as the foundation for our RAG application. It's a vector database designed specifically for storing and retrieving vast amounts of data represented as numerical vectors or embeddings. These embeddings capture the semantic meaning of text, enabling Chroma to perform rapid searches based on similarity, rather than exact keyword matches.

**Why Chroma is Crucial for GenAI Applications**

GenAI applications, like chatbots, question-answering systems, and recommendation engines, rely heavily on processing and understanding information quickly and accurately. Chroma plays a critical role in this process by offering several advantages:

- Efficient Information Retrieval: Chroma's vector-based search allows for rapid retrieval of relevant information based on semantic similarity. This is crucial for providing accurate and contextually relevant responses.
- Knowledge Base Management: GenAI models often require access to a large knowledge base. Chroma can efficiently store and manage this knowledge, making it readily available for the model to access.
- Real-time Performance: Chroma is optimized for speed, enabling real-time interactions with users. This is essential for applications that require immediate responses, such as chatbots or virtual assistants.
- Scalability: As the amount of data grows, Chroma can scale to handle increasing workloads, ensuring the continued performance of the GenAI application.

In essence, Chroma empowers GenAI applications to deliver exceptional performance and user experiences by effectively managing and accessing information.

## Building a RAG App with Gemini Pro API

Now, let's get hands-on and build a RAG application using Chroma and Gemini Pro. We'll cover the installation process, explore code examples, and see how these tools work together.

**Installation**


```python
!pip install -U -q google-generativeai   
!pip install -q chromadb
```

**Import packages**


```python
import textwrap
import chromadb
import numpy as np
import pandas as pd

import google.generativeai as genai

from IPython.display import Markdown
from chromadb import Documents, EmbeddingFunction, Embeddings
```

**Setup API key**
Put Gemini API key in .env under current folder,
```
GOOGLE_API_KEY=xxx
```


```python
import os

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
```

**list supported embedding models**


```python
for m in genai.list_models():
  if 'embedContent' in m.supported_generation_methods:
    print(m.name)
```

    models/embedding-001
    models/text-embedding-004


**Sample data**

We use documents list to hold reference document, each item is a string, represents one short text document or chunk of long text document.


```python
DOCUMENT1 = "Gemini is the result of large-scale collaborative efforts by teams across Google, including our colleagues at Google Research. It was built from the ground up to be multimodal, which means it can generalize and seamlessly understand, operate across and combine different types of information including text, code, audio, image and video."
DOCUMENT2 = "We designed Gemini to be natively multimodal, pre-trained from the start on different modalities. Then we fine-tuned it with additional multimodal data to further refine its effectiveness. This helps Gemini seamlessly understand and reason about all kinds of inputs from the ground up, far better than existing multimodal models — and its capabilities are state of the art in nearly every domain."
DOCUMENT3 = "Gemini has the most comprehensive safety evaluations of any Google AI model to date, including for bias and toxicity. We’ve conducted novel research into potential risk areas like cyber-offense, persuasion and autonomy, and have applied Google Research’s best-in-class adversarial testing techniques to help identify critical safety issues in advance of Gemini’s deployment."
documents = [DOCUMENT1, DOCUMENT2, DOCUMENT3]
documents
```




    ['Gemini is the result of large-scale collaborative efforts by teams across Google, including our colleagues at Google Research. It was built from the ground up to be multimodal, which means it can generalize and seamlessly understand, operate across and combine different types of information including text, code, audio, image and video.',
     'We designed Gemini to be natively multimodal, pre-trained from the start on different modalities. Then we fine-tuned it with additional multimodal data to further refine its effectiveness. This helps Gemini seamlessly understand and reason about all kinds of inputs from the ground up, far better than existing multimodal models — and its capabilities are state of the art in nearly every domain.',
     'Gemini has the most comprehensive safety evaluations of any Google AI model to date, including for bias and toxicity. We’ve conducted novel research into potential risk areas like cyber-offense, persuasion and autonomy, and have applied Google Research’s best-in-class adversarial testing techniques to help identify critical safety issues in advance of Gemini’s deployment.']



**Embeddings with model embedding-001**


```python
class GeminiEmbeddingFunction(EmbeddingFunction):
  def __call__(self, input: Documents) -> Embeddings:
    model = 'models/embedding-001'
    title = "Custom query"
    return genai.embed_content(model=model,
                                content=input,
                                task_type="retrieval_document",
                                title=title)["embedding"]
```

This is a custom class named `GeminiEmbeddingFunction` that implements the `EmbeddingFunction` interface. This class is designed to interact with the Gemini language model to generate embeddings for text documents.

1. **Class Definition:**

   - `GeminiEmbeddingFunction(EmbeddingFunction)`: This line declares the class `GeminiEmbeddingFunction` and indicates that it inherits from the `EmbeddingFunction` class. This means it must implement the `__call__` method.

2. **`__call__` Method:**

   - `def __call__(self, input: Documents) -> Embeddings`: This is the method that is called when an instance of the class is used as a function. It takes an `input` parameter of type `Documents` (which is presumably a data structure representing a list of documents) and returns an `Embeddings` object.

3. **Model Selection:**

   - `model = 'models/embedding-001'`: This line sets the `model` variable to the string 'models/embedding-001'. This likely refers to a specific embedding model within the Gemini language model framework.

4. **Title Setting:**

   - `title = "Custom query"`: This line sets the `title` variable to the string "Custom query". This might be used as a metadata field for the embedding.

5. **Embedding Generation:**

   - `return genai.embed_content(model=model, content=input, task_type="retrieval_document", title=title)["embedding"]`: This line calls the `genai.embed_content` function from the `genai` module. It passes the following arguments:
     - `model`: The selected embedding model ('models/embedding-001').
     - `content`: The input documents to be embedded.
     - `task_type`: Specifies the task for which the embeddings are being generated. In this case, it's set to "retrieval_document", indicating that the embeddings will be used for document retrieval.
     - `title`: The custom title for the embedding.
   - The function returns a dictionary containing the embeddings and other metadata. The code extracts the 'embedding' key from this dictionary and returns it as the result of the `__call__` method.

We define a function that can be used to generate embeddings for a list of documents using the Gemini language model. The embeddings can then be used for various tasks, such as semantic search or document similarity calculations.


**Create chroma db**


```python
def create_chroma_db(documents, name):
  chroma_client = chromadb.Client()
  db = chroma_client.create_collection(name=name, embedding_function=GeminiEmbeddingFunction())

  for i, d in enumerate(documents):
    db.add(
      documents=d,
      ids=str(i)
    )
  return db
```

**Setup vector db**

list and clean up old db


```python
client = chromadb.Client()
```


```python
collections = client.list_collections
client.list_collections()
```




    [Collection(name=geminidb)]




```python
for collection_name in (collection.name for collection in collections()):
    print(collection_name.strip())
```

    geminidb



```python
for collection_name in (collection.name for collection in collections()):
    if collection_name.strip() == "geminidb":
        print("Collection 'geminidb' exists, will remove it.")
        client.delete_collection(name="geminidb")
    else:
        print("Collection 'geminidb' does not exist.")
```

    Collection 'geminidb' exists, will remove it.



```python
client.list_collections()
```




    []




```python
db = create_chroma_db(documents, "geminidb")
```

**Verify db**

You might find embeddings is None from db.get(). When using get or query you can use the include parameter to specify which data you want returned - any of embeddings, documents, metadatas, and for query, distances. By default, Chroma will return the documents, metadatas and in the case of query, the distances of the results. embeddings are excluded by default for performance and the ids are always returned.


```python
db.get(include=['embeddings', 'documents', 'metadatas'])
```


```python
{'ids': ['0', '1', '2'],
 'embeddings': [[0.04447142407298088,
   -0.052165351808071136,
   -0.061552658677101135,
......
   -0.04504038393497467,
   0.005292229354381561]],
 'metadatas': [None, None, None],
 'documents': ['Gemini is the result of large-scale collaborative efforts by teams across Google, including our colleagues at Google Research. It was built from the ground up to be multimodal, which means it can generalize and seamlessly understand, operate across and combine different types of information including text, code, audio, image and video.',
  'We designed Gemini to be natively multimodal, pre-trained from the start on different modalities. Then we fine-tuned it with additional multimodal data to further refine its effectiveness. This helps Gemini seamlessly understand and reason about all kinds of inputs from the ground up, far better than existing multimodal models — and its capabilities are state of the art in nearly every domain.',
  'Gemini has the most comprehensive safety evaluations of any Google AI model to date, including for bias and toxicity. We’ve conducted novel research into potential risk areas like cyber-offense, persuasion and autonomy, and have applied Google Research’s best-in-class adversarial testing techniques to help identify critical safety issues in advance of Gemini’s deployment.'],
 'uris': None,
 'data': None}
```


```python
db.get(include=['embeddings', 'documents', 'metadatas'])['embeddings']
```


```python
pd.DataFrame(db.peek(3))
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ids</th>
      <th>embeddings</th>
      <th>metadatas</th>
      <th>documents</th>
      <th>uris</th>
      <th>data</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>[0.04447142407298088, -0.052165351808071136, -...</td>
      <td>None</td>
      <td>Gemini is the result of large-scale collaborat...</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>[0.05980474501848221, -0.05400879308581352, -0...</td>
      <td>None</td>
      <td>We designed Gemini to be natively multimodal, ...</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>[0.017100121825933456, -0.06025487929582596, -...</td>
      <td>None</td>
      <td>Gemini has the most comprehensive safety evalu...</td>
      <td>None</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
</div>



**Getting the relevant document**


```python
def get_relevant_passage(query, db):
  passage = db.query(query_texts=[query], n_results=1)['documents'][0][0]
  return passage
```

**Perform embedding search**


```python
passage = get_relevant_passage("safety", db)
Markdown(passage)
```




Gemini has the most comprehensive safety evaluations of any Google AI model to date, including for bias and toxicity. We’ve conducted novel research into potential risk areas like cyber-offense, persuasion and autonomy, and have applied Google Research’s best-in-class adversarial testing techniques to help identify critical safety issues in advance of Gemini’s deployment.



**Make a prompt**


```python
def make_prompt(query, relevant_passage):
  escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
  prompt = ("""You are a helpful and informative bot that answers questions using text from the reference passage included below. \
  Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
  However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
  strike a friendly and converstional tone. \
  If the passage is irrelevant to the answer, you may ignore it.
  QUESTION: '{query}'
  PASSAGE: '{relevant_passage}'

    ANSWER:
  """).format(query=query, relevant_passage=escaped)

  return prompt
```

**Pass a query to the prompt**


```python
query = "what is safety evaluations for gemini?"
prompt = make_prompt(query, passage)
Markdown(prompt)
```




You are a helpful and informative bot that answers questions using text from the reference passage included below.   Be sure to respond in a complete sentence, being comprehensive, including all relevant background information.   However, you are talking to a non-technical audience, so be sure to break down complicated concepts and   strike a friendly and converstional tone.   If the passage is irrelevant to the answer, you may ignore it.
  QUESTION: 'what is safety evaluations for gemini?'
  PASSAGE: 'Gemini has the most comprehensive safety evaluations of any Google AI model to date, including for bias and toxicity. We’ve conducted novel research into potential risk areas like cyber-offense, persuasion and autonomy, and have applied Google Research’s best-in-class adversarial testing techniques to help identify critical safety issues in advance of Gemini’s deployment.'

    ANSWER:
  



**Generate a response**


```python
model = genai.GenerativeModel('gemini-pro')
answer = model.generate_content(prompt)
Markdown(answer.text)
```




Gemini, a Google AI model, has undergone rigorous safety evaluations to ensure its responsible use. These evaluations encompass a wide range of potential risks, such as bias, toxicity, and even the possibility of misuse for offensive or manipulative purposes. To mitigate these risks, Google Research has employed advanced adversarial testing techniques to identify and address critical safety issues before Gemini's deployment.



## Build RAG chatbot using Chroma - wraping to class for easy integration 

**GeminiEmbeddingFunction**: This class defines a custom function to generate embeddings for the input documents using Google's generative AI model.

**RAGChatBot**: This class represents the core of the chatbot functionality.

- __init__: Initializes various properties like environment path, database name, list of documents, subject, embedding function, query, passage, model name, model object, chat history, and a ChromaDB client object.
- create_chroma_db: Creates a ChromaDB collection named geminidb (or deletes an existing one) and adds the provided documents with their IDs.
- get_relevant_passage: Retrieves the most relevant document (passage) from the ChromaDB collection based on the user's query.
- make_prompt: Constructs a formatted prompt for the generative model, including the user's question, the retrieved passage, and other information.
- log_chat_history: Saves the chat history to a text file with a timestamp.
- ragchat: The main function that drives the chatbot interaction:

**Main Execution**:

- Creates an instance of the RAGChatBot class.
- Defines sample documents and sets the subject.
- Assigns the documents and subject to the chatbot instance.
- Calls the ragchat function on the chatbot instance to initiate the conversation.

We implement a Retrieval-Augmented Generation (RAG) based chatbot that utilizes Google's generative AI model to answer user questions in a comprehensive and informative way, considering relevant information from a provided document set



```python
# gemini-rag-chatbot.py
# - Generative AI Gemini Chatbot
# - RAG Chatbot using ChromaDB
# @robertluwang
# Aug 2024

import textwrap
import chromadb
import numpy as np
import pandas as pd
import datetime

import google.generativeai as genai

from chromadb import Documents, EmbeddingFunction, Embeddings

import os

from dotenv import load_dotenv

class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        model = 'models/embedding-001'
        title = "Custom query"
        return genai.embed_content(model=model,
                                   content=input,
                                   task_type="retrieval_document",
                                   title=title)["embedding"]
class RAGChatBot:
    def __init__(self):
        self.envpath = '~'
        self.envfile = '.env'

        if self.envpath == '~':
            self.envpath = os.path.expanduser("~")
        
        load_dotenv(os.path.join(self.envpath, self.envfile))

        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        self.dbname = 'geminidb'
        self.db = None
        self.documents = []
        self.subject = ''
        self.embedding_function = GeminiEmbeddingFunction()
        self.query = ''
        self.passage = ''
        self.model_name = 'gemini-1.5-flash'
        self.model = genai.GenerativeModel(self.model_name)
        self.chat_history = []

        self.chroma_client = chromadb.Client() 

    def create_chroma_db(self):
        collections = self.chroma_client.list_collections
        for collection_name in (collection.name for collection in collections()):
            if collection_name.strip() == self.dbname:
                #print(f"Collection '{self.dbname}' exists, will remove it.")
                self.chroma_client.delete_collection(name=self.dbname)
        
        self.db = self.chroma_client.create_collection(name=self.dbname, embedding_function=self.embedding_function)
        
        for i, d in enumerate(self.documents):
            self.db.add(
              documents=d,
              ids=str(i)
            )
        return self.db
   
    def get_relevant_passage(self):
      self.passage = self.db.query(query_texts=[self.query], n_results=1)['documents'][0][0]
      return self.passage

    def make_prompt(self):
      escaped = self.passage.replace("'", "").replace('"', "").replace("\n", " ")
      prompt = ("""You are a helpful and informative bot that answers questions using text from the reference passage included below.\
      Be sure to respond in a complete sentence, being comprehensive, including all relevant background information.\
      However, you are talking to a non-technical audience, so be sure to break down complicated concepts and\
      strike a friendly and converstional tone.\
      If the passage is irrelevant to the answer, you may ignore it.
      QUESTION: '{query}'
      PASSAGE: '{passage}'
      ANSWER:
      """).format(query=self.query, passage=escaped)

      return prompt
        
    def log_chat_history(self,logpath):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"chat-log-{timestamp}.txt"
        log_path = os.path.join(logpath, log_filename)

        os.makedirs(logpath, exist_ok=True)

        with open(log_path, "w") as f:
            for message in self.chat_history:
                f.write(f"{message}\n")
        
        print(f"chat log file: {log_path}")
        
    def ragchat(self):

        self.db = self.create_chroma_db()

        n=1 # input number
        print("Welcome to Gemini RAG Chatbot ! ('/q' to exit)")
        self.chat_history.append(f"Welcome to Gemini RAG Chatbot ! ('/q' to exit)")
        print(f"Based on doc set of subject: '{self.subject}'\n")
        self.chat_history.append(f"Based on doc set of subject: '{self.subject}'\n")
        while True:
            self.query = input(f"{n} You: ")

            if not self.query:  # Check if input is empty (only Enter pressed)
                continue  # Skip processing empty input
            
            self.chat_history.append(f"{n} You: {self.query}\n")
                
            if self.query.lower() == "/q":
                self.log_chat_history('./log')
                print("Chat history saved. Exiting.")
                break
            
            self.passage = self.get_relevant_passage()

            prompt = self.make_prompt()
            print(f"prompt: {prompt}\n")

            response = self.model.generate_content(prompt)
            print(f"{n} RAG Chatbot: {response.text}")
            self.chat_history.append(f"{n} RAG Chatbot: {response.text}")
            n += 1

if __name__ == "__main__":
    ragchatbot = RAGChatBot()

    #ragchatbot.model_name = "gemini-1.5-flash"
    #ragchatbot.dbname = "geminidb"
    DOCUMENT1 = "Gemini is the result of large-scale collaborative efforts by teams across Google, including our colleagues at Google Research. It was built from the ground up to be multimodal, which means it can generalize and seamlessly understand, operate across and combine different types of information including text, code, audio, image and video."
    DOCUMENT2 = "We designed Gemini to be natively multimodal, pre-trained from the start on different modalities. Then we fine-tuned it with additional multimodal data to further refine its effectiveness. This helps Gemini seamlessly understand and reason about all kinds of inputs from the ground up, far better than existing multimodal models — and its capabilities are state of the art in nearly every domain."
    DOCUMENT3 = "Gemini has the most comprehensive safety evaluations of any Google AI model to date, including for bias and toxicity. We’ve conducted novel research into potential risk areas like cyber-offense, persuasion and autonomy, and have applied Google Research’s best-in-class adversarial testing techniques to help identify critical safety issues in advance of Gemini’s deployment."
    ragchatbot.documents = [DOCUMENT1, DOCUMENT2, DOCUMENT3]
    ragchatbot.subject = 'Gemini intro'

    ragchatbot.ragchat()
```

    Welcome to Gemini RAG Chatbot ! ('/q' to exit)
    Based on doc set of subject: 'Gemini intro'
    


    1 You:  safety


    prompt: You are a helpful and informative bot that answers questions using text from the reference passage included below.      Be sure to respond in a complete sentence, being comprehensive, including all relevant background information.      However, you are talking to a non-technical audience, so be sure to break down complicated concepts and      strike a friendly and converstional tone.      If the passage is irrelevant to the answer, you may ignore it.
          QUESTION: 'safety'
          PASSAGE: 'Gemini has the most comprehensive safety evaluations of any Google AI model to date, including for bias and toxicity. We’ve conducted novel research into potential risk areas like cyber-offense, persuasion and autonomy, and have applied Google Research’s best-in-class adversarial testing techniques to help identify critical safety issues in advance of Gemini’s deployment.'
          ANSWER:
          
    
    1 RAG Chatbot: Gemini has undergone extensive safety evaluations, more than any other Google AI model before it, to ensure its responsible use. 
    


    2 You:  /q


    chat log file: ./log/chat-log-2024-08-25_00-13-03.txt
    Chat history saved. Exiting.


## Conclusion

This blog has demonstrated how Chroma and Gemini Pro can be combined to create a powerful RAG application. By leveraging Chroma's efficient information retrieval capabilities and Gemini Pro's advanced language understanding, we can build intelligent applications that can answer questions, generate creative text formats, and provide informative summaries. As GenAI technology continues to evolve, the potential for building even more sophisticated and user-friendly applications becomes increasingly exciting.

## About Me
Hey! I am Robert Wang, live in Montreal.

More simple and more efficient.

- [GitHub: robertluwang](https://github.com/robertluwang)
- [Twitter: robertluwang](https://twitter.com/robertluwang)
- [LinkedIn: robertluwang](https://www.linkedin.com/in/robertluwang/)
- [Medium: robertluwang](https://medium.com/@robertluwang)
- [Dev.to: robertluwang](https://dev.to/robertluwang)
- [Web: dreamcloud.artark.ca](https://dreamcloud.artark.ca/)
