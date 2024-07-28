# Gemini embeddings demo

## What is text embedding

A list of floating point numbers that represent the meaning of a word, sentence, or paragraph


```python
!pip install -q -U google-generativeai
```

## Setup API key
Store your Google API key in .env under current folder:
GOOGLE_API_KEY=xxx


```python
import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
```

## Embed content
- model: `models/text-embedding-004`
- embed call: `embed_content`


```python
text = "Happy everyday!"
result = genai.embed_content(model="models/text-embedding-004", content=text)

# Print just a part of the embedding to keep the output manageable
print(str(result['embedding'])[:50], '... TRIMMED]')
```

    [-0.03669632, -0.029696692, -0.01009818, -0.016267 ... TRIMMED]



```python
print(len(result['embedding'])) 
```

    768


## Batch embed content

embed a list of multiple prompts with one API call for efficiency.


```python
result = genai.embed_content(
    model="models/text-embedding-004",
    content=[
      'What is genAI?',
      'What is your dinner plan?',
      'How does Zumba work for your body?'])

for embedding in result['embedding']:
  print(str(embedding)[:50], '... TRIMMED]')
```

    [-0.028737506, 0.049994964, -0.02702591, -0.059048 ... TRIMMED]
    [0.04651278, 0.01845331, 0.029534813, 0.01420539,  ... TRIMMED]
    [-0.011723411, 0.009849717, -0.020808367, -0.00312 ... TRIMMED]


## Truncating embeddings

Use `output_dimensionality` to truncate the output.


```python
# Not truncated
result1 = genai.embed_content(
    model="models/text-embedding-004",
    content="Postive thinking is key!")


# Truncated
result2 = genai.embed_content(
    model="models/text-embedding-004",
    content="Postive thinking is key!",
    output_dimensionality=10)


(len(result1['embedding']), len(result2['embedding']))
```




    (768, 10)



## Specify `task_type`

There are 5 parameters for the `embed_content` method: 

* `model`: Required. Must be `models/text-embedding-004` or `models/embedding-001`.
* `content`: Required. The content that you would like to embed.
* `task_type`: Optional. The task type for which the embeddings will be used.
* `title`: Optional. You should only set this parameter if your task type is `retrieval_document` (or `document`).
* `output_dimensionality`: Optional. Reduced dimension for the output embedding. If set, excessive values in the output embedding are truncated from the end. This is supported by `models/text-embedding-004`, but cannot be specified in `models/embedding-001`.

The following task_type parameters are accepted:

* `unspecified`: default to `retrieval_query`
* `retrieval_query` (or `query`): The given text is a query in a search/retrieval setting
* `retrieval_document` (or `document`): The given text is a document, Optionally, also set the `title` parameter with the title of the document
* `semantic_similarity` (or `similarity`): The given text will be used for Semantic Textual Similarity (STS)
* `classification`: The given text will be classified
* `clustering`: The embeddings used for clustering
* `question_answering`: The given text used for question answering
* `fact_verification`: The given text used for fact verification


```python
# Notice the API returns different embeddings depending on `task_type`
result1 = genai.embed_content(
    model="models/text-embedding-004",
    content="Postive thinking is key!")

result2 = genai.embed_content(
    model="models/text-embedding-004",
    content="Postive thinking is key!",
    task_type="document")

print(str(result1['embedding'])[:50], '... TRIMMED]')
print(str(result2['embedding'])[:50], '... TRIMMED]')
```

    [0.028295688, -0.06549204, -0.004657541, -0.058933 ... TRIMMED]
    [0.02249292, -0.03873647, -0.014411285, -0.0554903 ... TRIMMED]


## Further reading

* [Search Reranking](https://github.com/google-gemini/cookbook/blob/main/examples/Search_reranking_using_embeddings.ipynb): Use embeddings from the Gemini API to rerank search results from Wikipedia.

* [Anomaly detection with embeddings](https://github.com/google-gemini/cookbook/blob/main/examples/Anomaly_detection_with_embeddings.ipynb): Use embeddings from the Gemini API to detect potential outliers in your dataset.

* [Train a text classifier](https://github.com/google-gemini/cookbook/blob/main/examples/Classify_text_with_embeddings.ipynb): Use embeddings from the Gemini API to train a model that can classify different types of newsgroup posts based on the topic

* [Example with Chroma DB](https://github.com/google/generative-ai-docs/blob/main/examples/gemini/python/vectordb_with_chroma/vectordb_with_chroma.ipynb) Embeddings with Vector Databases

* [Embeddings guide](https://ai.google.dev/docs/embeddings_guide)  general embedding guide

* [Gemini API SDK](https://ai.google.dev/tutorials/python_quickstart#use_embeddings)

* [API reference embedContent](https://ai.google.dev/api/rest/v1/models/embedContent) and [batchEmbedContents](https://ai.google.dev/api/rest/v1/models/batchEmbedContents)
