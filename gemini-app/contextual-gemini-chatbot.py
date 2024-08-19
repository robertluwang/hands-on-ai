import google.generativeai as genai
import os
import datetime
from dotenv import load_dotenv
from os.path import expanduser

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
    chatbot.chat()