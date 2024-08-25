# dclib_py/ai/gemini.py
# Gemini AI tool sets
# - GeminiChatbot - general gemini chatbot
# - RAGChatBot - RAG chatbot using ChromaDB
# @robertluwang
# Aug 2024

import google.generativeai as genai
from dotenv import load_dotenv
from os.path import expanduser
import os
import datetime

import textwrap
import chromadb
import numpy as np
import pandas as pd
import datetime

from chromadb import Documents, EmbeddingFunction, Embeddings

def api_key(envpath='~', envfile='.env'):
    if envpath == '~':
        envpath = os.path.expanduser("~")
    
    load_dotenv(os.path.join(envpath, envfile))
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    return os.environ["GOOGLE_API_KEY"]

import pathlib
import textwrap

from IPython.display import display
from IPython.display import Markdown
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def list_models():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
class GeminiChatbot:
    def __init__(self):
        # Load the .env file from the home directory
        self.envpath = '~'
        self.envfile = '.env'

        if self.envpath == '~':
            self.envpath = os.path.expanduser("~")
        
        load_dotenv(os.path.join(self.envpath, self.envfile))

        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        self.modelname = "gemini-1.5-flash"
        self.model = genai.GenerativeModel(self.modelname)
        
        self.chat_history = []

    def generate_response(self, prompt):
        full_prompt = "Please go through chat history below if user ask question regarding on previous conversation.\nPlease anwser question directly if it is not related to previous conversation\n" + "+++chat history\n" + ''.join(self.chat_history) + "+++\n" + "new prompt: " + prompt
        response = self.model.generate_content(full_prompt)
        return response.text

    def log_chat_history(self,logpath):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"chat-log-{timestamp}.txt"
        log_path = os.path.join(logpath, log_filename)

        os.makedirs(logpath, exist_ok=True)

        with open(log_path, "w") as f:
            for message in self.chat_history:
                f.write(f"{message}\n")
        
        print(f"chat log file: {log_path}")
    
    def chat(self):
        n=1 # input number
        print("Welcome to GeminiChatbot! ('/q' to exit)\n")
        self.chat_history.append("Welcome to GeminiChatbot! ('/q' to exit)\n")
        while True:
            user_input = input(f"{n} You: ")
            self.chat_history.append(f"{n} You: {user_input}\n")
                      
            if user_input.lower() == "/q":
                self.log_chat_history('./log')
                print("Chat history saved. Exiting.")
                break
            response = self.generate_response(user_input)
            print(f"{n} Chatbot: {response}")
            self.chat_history.append(f"{n} Chatbot: {response}")
            n += 1

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
    chatbot = GeminiChatbot()
    #chatbot.envpath = '~' 
    #chatbot.envfile = '.env'
    #chatbot.modelname = "gemini-1.5-pro"
    chatbot.chat()