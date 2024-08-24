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
def create_chroma_db(documents, name, embedding_function=GeminiEmbeddingFunction()):
    """
    Creates a ChromaDB collection, generates embeddings for the documents using the provided embedding function, and adds the documents and embeddings to the collection.

    Args:
        documents (list): A list of documents to be added to the collection.
        name (str): The name of the collection.
        embedding_function (EmbeddingFunction, optional): The function used to generate embeddings for the documents. Defaults to GeminiEmbeddingFunction().

    Returns:
        chromadb.Collection: The created ChromaDB collection.
    """

    chroma_client = chromadb.Client()
    db = chroma_client.create_collection(name=name, embedding_function=GeminiEmbeddingFunction())

    # Generate embeddings
    embeddings = embedding_function(documents)
    print("Embeddings generated:", embeddings)

    # Verify data types
    if not isinstance(embeddings, list) or not all(isinstance(embedding, list) for embedding in embeddings):
        raise ValueError("Embeddings must be a list of lists of numbers.")

    if not all(isinstance(value, (int, float)) for embedding in embeddings for value in embedding):
        raise ValueError("Embedding elements must be numerical.")

    # Add documents and embeddings
    try:
        db.add(
            documents=documents,
            embeddings=embeddings,
            ids=[str(i) for i in range(len(documents))]
        )
        print("Documents and embeddings added successfully.")
    except Exception as e:
        print(f"Error adding documents and embeddings: {e}")

    return db
```

The `create_chroma_db` function creates a ChromaDB collection, generates embeddings for a list of documents using a specified embedding function, and adds both the documents and their corresponding embeddings to the collection.

1. **Function Definition:**
   - `def create_chroma_db(documents, name, embedding_function=GeminiEmbeddingFunction())`:
     - Defines a function named `create_chroma_db` that takes three arguments:
       - `documents`: A list of documents to be added to the collection.
       - `name`: The name to be given to the ChromaDB collection.
       - `embedding_function`: An optional argument specifying the function used to generate embeddings for the documents. If not provided, `GeminiEmbeddingFunction()` is used by default.

2. **ChromaDB Client and Collection Creation:**
   - `chroma_client = chromadb.Client()`: Creates an instance of the ChromaDB client.
   - `db = chroma_client.create_collection(name=name, embedding_function=GeminiEmbeddingFunction())`: Creates a new collection in the ChromaDB database with the specified `name` and uses the provided `embedding_function` to generate embeddings for the documents.

3. **Embedding Generation:**
   - `embeddings = embedding_function(documents)`: Calls the provided `embedding_function` on the `documents` list to generate embeddings for each document.

4. **Data Type Validation:**
   - `if not isinstance(embeddings, list) or not all(isinstance(embedding, list) for embedding in embeddings):`: Checks if the `embeddings` are a list of lists.
   - `if not all(isinstance(value, (int, float)) for embedding in embeddings for value in embedding):`: Checks if all elements within the embeddings are numerical (integers or floats).

5. **Document and Embedding Addition:**
   - `db.add(documents=documents, embeddings=embeddings, ids=[str(i) for i in range(len(documents))])`: Adds the documents and their corresponding embeddings to the ChromaDB collection. Unique identifiers are generated using a list comprehension for each document.

6. **Error Handling:**
   - A `try-except` block is used to catch any exceptions that might occur during the process of adding documents and embeddings to the collection.

7. **Collection Return:**
   - The newly created ChromaDB collection is returned.

**Key Points:**

- The function ensures that the embeddings are generated using the specified `embedding_function`.
- It validates the data types of the embeddings to ensure they are compatible with ChromaDB.
- It adds both the documents and their embeddings to the collection, using unique identifiers for each document.
- It includes error handling to catch potential exceptions during the process.

This function provides a robust and flexible way to create ChromaDB collections with custom embedding functions and data validation.


**Setup vector db**

list and clean up old db


```python
client = chromadb.Client()
```


```python
client.list_collections()
```




    [Collection(name=geminidb)]




```python
client.delete_collection(name="geminidb")
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




Google has performed the most comprehensive safety evaluations yet for Gemini, including assessments for bias and toxicity. Google uses advanced methods, including adversarial testing, to help identify possible safety issues before Gemini is released.



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
