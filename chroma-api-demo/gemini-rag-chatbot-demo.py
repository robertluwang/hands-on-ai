
import textwrap
import chromadb
import numpy as np
import pandas as pd

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
    #print("Embeddings generated:", embeddings)

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
        #print("Documents and embeddings added successfully.")
    except Exception as e:
        print(f"Error adding documents and embeddings: {e}")

    return db

def get_relevant_passage(query, db):
  passage = db.query(query_texts=[query], n_results=1)['documents'][0][0]
  return passage

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

def main():
  load_dotenv()

  genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

  DOCUMENT1 = "Gemini is the result of large-scale collaborative efforts by teams across Google, including our colleagues at Google Research. It was built from the ground up to be multimodal, which means it can generalize and seamlessly understand, operate across and combine different types of information including text, code, audio, image and video."
  DOCUMENT2 = "We designed Gemini to be natively multimodal, pre-trained from the start on different modalities. Then we fine-tuned it with additional multimodal data to further refine its effectiveness. This helps Gemini seamlessly understand and reason about all kinds of inputs from the ground up, far better than existing multimodal models — and its capabilities are state of the art in nearly every domain."
  DOCUMENT3 = "Gemini has the most comprehensive safety evaluations of any Google AI model to date, including for bias and toxicity. We’ve conducted novel research into potential risk areas like cyber-offense, persuasion and autonomy, and have applied Google Research’s best-in-class adversarial testing techniques to help identify critical safety issues in advance of Gemini’s deployment."
  documents = [DOCUMENT1, DOCUMENT2, DOCUMENT3]

  client = chromadb.Client()

  collections = client.list_collections

  for collection_name in (collection.name for collection in collections()):
    if "geminidb" in collection_name:
        print("Collection 'geminidb' exists, will remove it.")
        client.delete_collection(name="geminidb")
    else:
        print("Collection 'geminidb' does not exist.")

  db = create_chroma_db(documents, "geminidb")

  passage = get_relevant_passage("safety", db)
  #print(passage)

  query = "what is safety evaluations for gemini?"
  prompt = make_prompt(query, passage)
  #print(prompt)

  model = genai.GenerativeModel('gemini-pro')
  answer = model.generate_content(prompt)
  print(answer.text)

if __name__ == "__main__":
    main()
  



