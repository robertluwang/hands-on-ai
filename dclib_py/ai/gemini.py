import google.generativeai as genai
from dotenv import load_dotenv
from os.path import expanduser
import os
import datetime

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

if __name__ == "__main__":
    chatbot = GeminiChatbot()
    #chatbot.envpath = '~' 
    #chatbot.envfile = '.env'
    #chatbot.modelname = "gemini-1.5-pro"
    chatbot.chat()