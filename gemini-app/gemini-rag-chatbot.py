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

    def create_chroma_db(self):
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
        db = chroma_client.create_collection(name=self.dbname, embedding_function=self.embedding_function)

        # Generate embeddings
        embeddings = self.embedding_function(self.documents)
        #print("Embeddings generated:", embeddings)

        # Verify data types
        if not isinstance(embeddings, list) or not all(isinstance(embedding, list) for embedding in embeddings):
            raise ValueError("Embeddings must be a list of lists of numbers.")

        if not all(isinstance(value, (int, float)) for embedding in embeddings for value in embedding):
            raise ValueError("Embedding elements must be numerical.")

        # Add documents and embeddings
        try:
            db.add(
                documents=self.documents,
                embeddings=embeddings,
                ids=[str(i) for i in range(len(self.documents))]
            )
            #print("Documents and embeddings added successfully.")
        except Exception as e:
            print(f"Error adding documents and embeddings: {e}")

        return db

    def create_or_update_chroma_db(self):
        client = chromadb.Client()

        collections = client.list_collections()
        for collection_name in (collection.name for collection in collections()):
            if self.dbname in collection_name:
                print(f"Collection '{self.dbname}' exists.")
                return client.get_collection(self.dbname)
            else:
                print(f"Collection '{self.dbname}' does not exist.")

        print(f"Creating ChromaDB collection '{self.dbname}'...")
        return self.create_chroma_db(self)
    
    def get_relevant_passage(self):
      passage = self.db.query(query_texts=[self.query], n_results=1)['documents'][0][0]
      return passage

    def make_prompt(self,relevant_passage):
      escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
      prompt = ("""You are a helpful and informative bot that answers questions using text from the reference passage included below.\
      Be sure to respond in a complete sentence, being comprehensive, including all relevant background information.\
      However, you are talking to a non-technical audience, so be sure to break down complicated concepts and\
      strike a friendly and converstional tone.\
      If the passage is irrelevant to the answer, you may ignore it.
      QUESTION: '{query}'
      PASSAGE: '{relevant_passage}'
      ANSWER:
      """).format(query=self.query, relevant_passage=escaped)

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
            self.chat_history.append(f"{n} You: {self.query}\n")
                      
            if self.query.lower() == "/q":
                self.log_chat_history('./log')
                print("Chat history saved. Exiting.")
                break
            
            self.passage = self.get_relevant_passage()

            prompt = self.make_prompt(self.passage)
            print(f"prompt: {prompt}\n")

            response = self.model.generate_content(prompt)
            print(f"{n} Chatbot: {response.text}")
            self.chat_history.append(f"{n} Chatbot: {response.text}")
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


