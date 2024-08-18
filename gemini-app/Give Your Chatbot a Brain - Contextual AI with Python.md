# Give Your Chatbot a Brain - Contextual AI with Python
## Introduction

Imagine a conversation that feels more like talking to a friend and less like interacting with a machine. That's the power of a chatbot with a memory! In today's digital world, chatbots are everywhere, from answering customer service questions to providing companionship. But what truly sets a great chatbot apart? The ability to remember past conversations and tailor responses accordingly. This is where the magic of contextual chatbots comes in.

The most of popular LLM already supports contextual chatbot by including chat history, such as OpenAI and Gemini Pro, but not all of them. As education purpose, we implment a simple chat history chatbot using Gemini Pro.

This tutorial will guide you through building a secure and contextual Gemini chatbot using Python. We'll leverage the power of Google's generative AI library (google.generativeai) to create chat sessions that chatbot will remember. By incorporating memory into your chatbot, you'll design a more engaging and helpful experience.


## Gemini chat hostory demo


```python
import google.generativeai as genai
import os
import datetime
from dotenv import load_dotenv
from os.path import expanduser


envpath = '~'
envfile = '.env'

if envpath == '~':
    envpath = os.path.expanduser("~")

load_dotenv(os.path.join(envpath, envfile))

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

modelname = "gemini-1.5-flash"
model = genai.GenerativeModel(modelname)
```


```python
chat = model.start_chat(history=[])

response = chat.send_message('tell me a joke about AI')
print(response.text) 

response = chat.send_message('tell me another joke about AI')
print(response.text)
```

    Why did the AI get fired from its job at the library? 
    
    Because it was always getting lost in the stacks! 📚🤖 
    
    Why did the AI cross the road? 
    
    To get to the other *side* of the algorithm! 🤖 
    



```python
print(chat.history)
```

    [parts {
      text: "tell me a joke about AI"
    }
    role: "user"
    , parts {
      text: "Why did the AI get fired from its job at the library? \n\nBecause it was always getting lost in the stacks! 📚🤖 \n"
    }
    role: "model"
    , parts {
      text: "tell me a joke about AI"
    }
    role: "user"
    , parts {
      text: "Why did the AI cross the road? \n\nTo get to the other *side* of the algorithm! 🤖 \n"
    }
    role: "model"
    ]


From below test, we can see Gemini has memory of previous conversatoin.


```python
response = chat.send_message('what was 1st joke you told me?')

print(response.text) 
```

    You're right! I'm still under development, and I sometimes forget things like past conversations.  
    
    The first joke I told you was: 
    
    "Why did the AI get fired from its job at the library? Because it was always getting lost in the stacks!" 📚🤖 
    
    Let me know if you'd like to hear another one! 😄 
    



```python
for part in (chat.history):
    print(part.parts[0])
```

    text: "tell me a joke about AI"
    
    text: "Why did the AI get fired from its job at the library? \n\nBecause it was always getting lost in the stacks! 📚🤖 \n"
    
    text: "tell me a joke about AI"
    
    text: "Why did the AI cross the road? \n\nTo get to the other *side* of the algorithm! 🤖 \n"
    
    text: "what was 1st joke you told me?"
    
    text: "You\'re right! I\'m still under development, and I sometimes forget things like past conversations.  \n\nThe first joke I told you was: \n\n\"Why did the AI get fired from its job at the library? Because it was always getting lost in the stacks!\" 📚🤖 \n\nLet me know if you\'d like to hear another one! 😄 \n"
    


Let's create chat history feature without using default Gemini history[], this concept and approach will aplly for any LLM.

## Building the Chatbot Class

### Class Definition and Initialization


```python
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

        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)

        self.modelname = "gemini-1.5-flash"
        self.model = genai.GenerativeModel(self.modelname)
        
        self.chat_history = []

```

* **Class Definition:** The `GeminiChatbot` class encapsulates the chatbot's functionality.
* **.env File Loading:** By default, the `load_dotenv` function loads the `.env` file from the home directory, securely storing the API key. You can change to any envpath and envfile.
* **API Key Configuration:** The `os.getenv("GOOGLE_API_KEY")` retrieves the API key from the environment variable and configures the Gemini API.
* **Model Initialization:** By default, a `GenerativeModel` instance is created using the `gemini-1.5-flash` model, you can change to any Gemini model.
* **Chat History Initialization:** An empty list is created to store the chat history.


```python
chatbot = GeminiChatbot()
user_input = ("tell a joke about AI")
chatbot.chat_history.append(f"You: {user_input}")
response = chatbot.model.generate_content(user_input)
chatbot.chat_history.append(f"Chatbot: {response.text}")
print(response.text)
print(chatbot.chat_history)
```

    Why did the AI get fired from the dating app?
    
    Because it couldn't tell the difference between a "like" and a "dislike," and kept matching people with their worst enemies! 
    
    ['You: tell a joke about AI', 'Chatbot: Why did the AI get fired from the dating app?\n\nBecause it couldn\'t tell the difference between a "like" and a "dislike," and kept matching people with their worst enemies! \n']


### Generating Response


```python
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

        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)

        self.modelname = "gemini-1.5-flash"
        self.model = genai.GenerativeModel(self.modelname)
        
        self.chat_history = []

    def generate_response(self, prompt):
        full_prompt = "Please go through chat history below if user ask question regarding on previous conversation.\nPlease anwser question directly if it is not related to previous conversation\n" + "+++chat history\n" + ''.join(self.chat_history) + "+++\n" + "new prompt: " + prompt
        response = self.model.generate_content(full_prompt)
        return response.text
```

* The `generate_response` method takes a user prompt as input.
* The full combined prompt is concatenated with the chat history lookup rule, entire chat history and the current prompt to provide context for the response.
* The Gemini model generates a response based on the combined prompt.


```python
chatbot = GeminiChatbot()
user_input = ("tell a joke about AI")
chatbot.chat_history.append(f"You: {user_input}")
response = chatbot.generate_response(user_input)
chatbot.chat_history.append(f"Chatbot: {response}")
print(response)
```

    Why did the AI cross the road? 
    
    To get to the other *side* of the algorithm! 
    



```python
user_input = ("what was joke you told me?")
chatbot.chat_history.append(f"You: {user_input}")
response = chatbot.generate_response(user_input)
chatbot.chat_history.append(f"Chatbot: {response}")
print(response)
```

    The joke I told you was:
    
    Why did the AI cross the road? 
    
    To get to the other *side* of the algorithm! 
    



```python
print(chatbot.chat_history)
```

    ['You: tell a joke about AI', 'Chatbot: Why did the AI cross the road? \n\nTo get to the other *side* of the algorithm! \n', 'You: what was joke you told me?', 'Chatbot: The joke I told you was:\n\nWhy did the AI cross the road? \n\nTo get to the other *side* of the algorithm! \n']


### Logging Chat History


```python
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

        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)

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
```

* This method logs the chat history to a text file.
* A timestamp is generated to create a unique filename for the log.
* The log directory is created if it doesn't exist.
* The chat history is written to the log file, one message per line.


```python
chatbot = GeminiChatbot()
user_input = "tell a joke about AI"
chatbot.chat_history.append(f"You: {user_input}")
response = chatbot.generate_response(user_input)
chatbot.chat_history.append(f"Chatbot: {response}")
print(response)

user_input = "how are you today?"
chatbot.chat_history.append(f"You: {user_input}")
response = chatbot.generate_response(user_input)
chatbot.chat_history.append(f"Chatbot: {response}")
print(response)

user_input = "what was joke you told me?"
chatbot.chat_history.append(f"You: {user_input}")
response = chatbot.generate_response(user_input)
chatbot.chat_history.append(f"Chatbot: {response}")
print(response)

chatbot.log_chat_history('./log')
```

    Why did the AI cross the road? 
    
    To get to the other *side* of the algorithm! 
    
    I'm doing well, thank you for asking! How about you? 😊 
    
    You asked: "Why did the AI cross the road?" 
    
    And I answered: "To get to the other *side* of the algorithm!" 
    
    chat log file: ./log/chat-log-2024-08-18_12-54-43.txt



```python
chatbot.chat_history
```




    ['You: tell a joke about AI',
     'Chatbot: Why did the AI cross the road? \n\nTo get to the other *side* of the algorithm! \n',
     'You: how are you today?',
     "Chatbot: I'm doing well, thank you for asking! How about you? 😊 \n",
     'You: what was joke you told me?',
     'Chatbot: You asked: "Why did the AI cross the road?" \n\nAnd I answered: "To get to the other *side* of the algorithm!" \n']



### Using the Chatbot


```python
    def chat(self):
        print("Welcome to GeminiChatbot! ('/q' to exit)\n")
        self.chat_history.append("Welcome to GeminiChatbot! ('/q' to exit)\n")
        while True:
            user_input = input("You: ")
            self.chat_history.append(f"You: {user_input}\n")
                      
            if user_input.lower() == "/q":
                self.log_chat_history()
                print("Chat history saved. Exiting.")
                break
            response = self.generate_response(user_input)
            print(f"Chatbot: {response}")
            self.chat_history.append(f"Chatbot: {response}")

```

The chat function is main chatbot to end user:
* It enters a loop to continuously prompt the user for input.
* The chatbot generates responses based on the user's input and the chat history.
* When the user enters "/q", the chat history is logged and the program exits.

### Complete gemini chatbot app


```python
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

        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)

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


```

    Welcome to GeminiChatbot! ('/q' to exit)
    


    1 You:  hello


    1 Chatbot: Hello! 👋 How can I help you today? 
    


    2 You:  how are you?


    2 Chatbot: I'm doing well, thank you for asking! How can I help you today? 😊 
    


    3 You:  tell me a joke


    3 Chatbot: Why don't scientists trust atoms?
    
    Because they make up everything! 
    


    4 You:  tell me another joke


    4 Chatbot: Why don't they play poker in the jungle? 
    
    Too many cheetahs! 🐆 
    


    5 You:  what was 1st joke?


    5 Chatbot: The first joke was:  "Why don't scientists trust atoms? Because they make up everything!" 
    


    6 You:  what was 2nd joke?


    6 Chatbot: The second joke was: "Why don't they play poker in the jungle? Too many cheetahs!" 🐆 
    


    7 You:  what was 1st word I said?


    7 Chatbot: The first word you said was "hello". 
    


    8 You:  what was 2nd word I said?


    8 Chatbot: The second word you said was "how". 
    


    9 You:  what was 2nd question I asked?


    9 Chatbot: The second question you asked was "how are you?" 
    


    10 You:  /q


    chat log file: ./log/chat-log-2024-08-18_12-41-13.txt
    Chat history saved. Exiting.



```python
chatbot.chat_history
```




    ["Welcome to GeminiChatbot! ('/q' to exit)\n",
     '1 You: hello\n',
     '1 Chatbot: Hello! 👋 How can I help you today? \n',
     '2 You: how are you?\n',
     "2 Chatbot: I'm doing well, thank you for asking! How can I help you today? 😊 \n",
     '3 You: tell me a joke\n',
     "3 Chatbot: Why don't scientists trust atoms?\n\nBecause they make up everything! \n",
     '4 You: tell me another joke\n',
     "4 Chatbot: Why don't they play poker in the jungle? \n\nToo many cheetahs! 🐆 \n",
     '5 You: what was 1st joke?\n',
     '5 Chatbot: The first joke was:  "Why don\'t scientists trust atoms? Because they make up everything!" \n',
     '6 You: what was 2nd joke?\n',
     '6 Chatbot: The second joke was: "Why don\'t they play poker in the jungle? Too many cheetahs!" 🐆 \n',
     '7 You: what was 1st word I said?\n',
     '7 Chatbot: The first word you said was "hello". \n',
     '8 You: what was 2nd word I said?\n',
     '8 Chatbot: The second word you said was "how". \n',
     '9 You: what was 2nd question I asked?\n',
     '9 Chatbot: The second question you asked was "how are you?" \n',
     '10 You: /q\n']



### Change chatbot instance


```python
chatbot = GeminiChatbot()
chatbot.envpath = "/mnt/c/dclab/dev/ai-ml"
chatbot.modelname = "gemini-1.5-pro"
chatbot.chat()
```

    Welcome to GeminiChatbot! ('/q' to exit)
    


    1 You:  hello


    1 Chatbot: Hello! 👋 How can I help you today? 😊 
    


    2 You:  tell me a joke


    2 Chatbot: Why don't scientists trust atoms? 
    
    Because they make up everything! 
    


    3 You:  tell me another joke


    3 Chatbot: Why don't they play poker in the jungle? 
    
    Too many cheetahs! 🐆 
    


    4 You:  what was 1st joke?


    4 Chatbot: The first joke was: 
    
    Why don't scientists trust atoms? 
    
    Because they make up everything! 
    


    5 You:  what was 2nd joke?


    5 Chatbot: The second joke was:
    
    Why don't they play poker in the jungle? 
    
    Too many cheetahs! 🐆 
    


    6 You:  what was 1st word I said?


    6 Chatbot: The first word you said was "hello". 
    


    7 You:  /q


    chat log file: ./log/chat-log-2024-08-18_12-42-19.txt
    Chat history saved. Exiting.



```python
chatbot.chat_history
```

## Conclusion

Why is memory so important for chatbots? Just like real conversations, remembering past interactions allows chatbots to provide more relevant and personalized responses. In this blog, we've built a Gemini chatbot using Python that can summarize chat history and use that context to inform its responses. This approach leads to a more natural and engaging conversation for the user.

By following these steps and using the google.generativeai library, you can create a robust and contextual Gemini chatbot that users will enjoy interacting with. Remember to replace 'YOUR_API_KEY' with your actual Gemini API key in the .env file. With this foundation, you can extend your chatbot's capabilities and create truly memorable chat experiences.


```python

```
