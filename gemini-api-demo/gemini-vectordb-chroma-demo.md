# Gemini Vectordb Chroma demo

##  Install api and chromadb


```python
!pip install -U -q google-generativeai
!pip install -q chromadb
```


```python
import textwrap
import chromadb
import numpy as np
import pandas as pd

import google.generativeai as genai

from IPython.display import Markdown
from chromadb import Documents, EmbeddingFunction, Embeddings
```

## Setup API key



```python
import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
```

## Embedding model


```python
for m in genai.list_models():
  if 'embedContent' in m.supported_generation_methods:
    print(m.name)
```

    models/embedding-001
    models/text-embedding-004


## Data

A small set of documents to create an embedding database:


```python
DOCUMENT1 = "Operating the Climate Control System  Your Googlecar has a climate control system that allows you to adjust the temperature and airflow in the car. To operate the climate control system, use the buttons and knobs located on the center console.  Temperature: The temperature knob controls the temperature inside the car. Turn the knob clockwise to increase the temperature or counterclockwise to decrease the temperature. Airflow: The airflow knob controls the amount of airflow inside the car. Turn the knob clockwise to increase the airflow or counterclockwise to decrease the airflow. Fan speed: The fan speed knob controls the speed of the fan. Turn the knob clockwise to increase the fan speed or counterclockwise to decrease the fan speed. Mode: The mode button allows you to select the desired mode. The available modes are: Auto: The car will automatically adjust the temperature and airflow to maintain a comfortable level. Cool: The car will blow cool air into the car. Heat: The car will blow warm air into the car. Defrost: The car will blow warm air onto the windshield to defrost it."
DOCUMENT2 = "Your Googlecar has a large touchscreen display that provides access to a variety of features, including navigation, entertainment, and climate control. To use the touchscreen display, simply touch the desired icon.  For example, you can touch the \"Navigation\" icon to get directions to your destination or touch the \"Music\" icon to play your favorite songs."
DOCUMENT3 = "Shifting Gears Your Googlecar has an automatic transmission. To shift gears, simply move the shift lever to the desired position.  Park: This position is used when you are parked. The wheels are locked and the car cannot move. Reverse: This position is used to back up. Neutral: This position is used when you are stopped at a light or in traffic. The car is not in gear and will not move unless you press the gas pedal. Drive: This position is used to drive forward. Low: This position is used for driving in snow or other slippery conditions."

documents = [DOCUMENT1, DOCUMENT2, DOCUMENT3]
```

## Creating the embedding database with ChromaDB

- create a [custom function](https://docs.trychroma.com/embeddings#custom-embedding-functions){:.external} 
- input a set of documents into this custom function
- receive vectors, or embeddings of the documents


### API changes to Embeddings with model embedding-001

For the new embeddings model, embedding-001, there is a new task type parameter and the optional title (only valid with task_type=`RETRIEVAL_DOCUMENT`).

These new parameters apply only to the newest embeddings models.The task types are:

Task Type | Description
---       | ---
RETRIEVAL_QUERY	| Specifies the given text is a query in a search/retrieval setting.
RETRIEVAL_DOCUMENT | Specifies the given text is a document in a search/retrieval setting.
SEMANTIC_SIMILARITY	| Specifies the given text will be used for Semantic Textual Similarity (STS).
CLASSIFICATION	| Specifies that the embeddings will be used for classification.
CLUSTERING	| Specifies that the embeddings will be used for clustering.


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

### Create the vector database
- In the `create_chroma_db` function, instantiate a [Chroma client](https://docs.trychroma.com/getting-started){:.external}
- Create a collection to store embeddings/documents/metadata
- Pass above embedding function as an argument to the `create_collection`
- Use the `add` method to add the documents to the collection


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


```python
# Set up the DB
db = create_chroma_db(documents, "googlecarsdatabase")
```

Confirm that the data was inserted by looking at the database:


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
      <td>[-0.020994942635297775, -0.03876612335443497, ...</td>
      <td>None</td>
      <td>Operating the Climate Control System  Your Goo...</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>[0.017410801723599434, -0.04757162556052208, -...</td>
      <td>None</td>
      <td>Your Googlecar has a large touchscreen display...</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>[-0.03194405511021614, -0.023281503468751907, ...</td>
      <td>None</td>
      <td>Shifting Gears Your Googlecar has an automatic...</td>
      <td>None</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
</div>



## Getting the relevant document

- `db` is a Chroma collection object
- call `query` on it to perform a nearest neighbors search to find similar embeddings or documents



```python
def get_relevant_passage(query, db):
  passage = db.query(query_texts=[query], n_results=1)['documents'][0][0]
  return passage
```


```python
# Perform embedding search
passage = get_relevant_passage("touch screen features", db)
Markdown(passage)
```




Your Googlecar has a large touchscreen display that provides access to a variety of features, including navigation, entertainment, and climate control. To use the touchscreen display, simply touch the desired icon.  For example, you can touch the "Navigation" icon to get directions to your destination or touch the "Music" icon to play your favorite songs.



found the relevant passage in set of documents, use it make a prompt to pass into the Gemini API.


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

Pass a query to the prompt:


```python
query = "How do you use the touchscreen in the Google car?"
prompt = make_prompt(query, passage)
Markdown(prompt)
```




You are a helpful and informative bot that answers questions using text from the reference passage included below.   Be sure to respond in a complete sentence, being comprehensive, including all relevant background information.   However, you are talking to a non-technical audience, so be sure to break down complicated concepts and   strike a friendly and converstional tone.   If the passage is irrelevant to the answer, you may ignore it.
  QUESTION: 'How do you use the touchscreen in the Google car?'
  PASSAGE: 'Your Googlecar has a large touchscreen display that provides access to a variety of features, including navigation, entertainment, and climate control. To use the touchscreen display, simply touch the desired icon.  For example, you can touch the Navigation icon to get directions to your destination or touch the Music icon to play your favorite songs.'

    ANSWER:
  



Now use the `generate_content` method to to generate a response from the model.


```python
model = genai.GenerativeModel('gemini-1.5-flash-latest')
answer = model.generate_content(prompt)
Markdown(answer.text)
```




The Google car's touchscreen is easy to use!  Just tap the icon for whatever you want to do, like navigation, music, or climate control.  For example, to get directions, tap the Navigation icon, and to listen to music, tap the Music icon. 



