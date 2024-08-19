```python
import sys
sys.path.append('..')

import dclib_py.ai.gemini as dcgm
```


```python
dcgm.api_key()
```


```python
dcgm.list_models()
```

    models/gemini-1.0-pro-latest
    models/gemini-1.0-pro
    models/gemini-pro
    models/gemini-1.0-pro-001
    models/gemini-1.0-pro-vision-latest
    models/gemini-pro-vision
    models/gemini-1.5-pro-latest
    models/gemini-1.5-pro-001
    models/gemini-1.5-pro
    models/gemini-1.5-pro-exp-0801
    models/gemini-1.5-flash-latest
    models/gemini-1.5-flash-001
    models/gemini-1.5-flash
    models/gemini-1.5-flash-001-tuning



```python
model = dcgm.genai.GenerativeModel('gemini-1.5-flash')
```


```python
response = model.generate_content("tell a joke about AI")
print(response.text)
```

    Why did the AI get fired from its job at the library? 
    
    Because it was always getting lost in the Dewey Decimal System! 
    



```python
response
```




    response:
    GenerateContentResponse(
        done=True,
        iterator=None,
        result=protos.GenerateContentResponse({
          "candidates": [
            {
              "content": {
                "parts": [
                  {
                    "text": "Why did the AI get fired from its job at the library? \n\nBecause it was always getting lost in the Dewey Decimal System! \n"
                  }
                ],
                "role": "model"
              },
              "finish_reason": "STOP",
              "index": 0,
              "safety_ratings": [
                {
                  "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                  "probability": "NEGLIGIBLE"
                },
                {
                  "category": "HARM_CATEGORY_HATE_SPEECH",
                  "probability": "NEGLIGIBLE"
                },
                {
                  "category": "HARM_CATEGORY_HARASSMENT",
                  "probability": "NEGLIGIBLE"
                },
                {
                  "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                  "probability": "NEGLIGIBLE"
                }
              ]
            }
          ],
          "usage_metadata": {
            "prompt_token_count": 6,
            "candidates_token_count": 27,
            "total_token_count": 33
          }
        }),
    )




```python
dcgm.to_markdown(response.text)
```




> Why did the AI get fired from its job at the library? 
> 
> Because it was always getting lost in the Dewey Decimal System! 





```python
response = model.generate_content("What is genAI?", stream=True)
```


```python
for chunk in response:
  print(chunk.text)
  print("_"*80)
```

    ##
    ________________________________________________________________________________
     GenAI: The Art of Artificial Intelligence Creativity
    
    GenAI, short for **
    ________________________________________________________________________________
    Generative Artificial Intelligence**, is a subset of AI that focuses on creating new content
    ________________________________________________________________________________
    , like:
    
    * **Text:** Writing articles, poems, code, scripts, and more. 
    * **Images:** Creating realistic or stylized images from
    ________________________________________________________________________________
     text descriptions.
    * **Audio:** Generating music, speech, and sound effects.
    * **Video:** Producing videos and animations.
    * **3D
    ________________________________________________________________________________
     Models:** Building complex 3D objects.
    
    GenAI models are trained on vast amounts of data and learn patterns within it. They can then use this knowledge to generate new content that is similar to the data they were trained on. 
    ________________________________________________________________________________
    
    
    Here are some key aspects of GenAI:
    
    * **Creativity:** GenAI models can produce novel and unique content, going beyond simply mimicking existing work.
    * **Efficiency:** They can generate content much faster than humans, saving time
    ________________________________________________________________________________
     and resources.
    * **Customization:** Users can often control the parameters of the generation process to tailor the output to their specific needs.
    
    **Examples of GenAI applications:**
    
    * **ChatGPT:** A language model that generates human-like text for conversations.
    * **DALL-E 2:** A
    ________________________________________________________________________________
     model that creates images from text descriptions.
    * **Stable Diffusion:** An open-source image generation model.
    * **Jukebox:** A model that generates music in different genres and styles.
    * **Midjourney:** A popular AI art generator accessible through a Discord server.
    
    **Potential benefits of GenAI:**
    ________________________________________________________________________________
    
    
    * **Increased productivity:** Automating content creation tasks.
    * **Enhanced creativity:** Enabling new forms of artistic expression.
    * **Personalized experiences:** Generating tailored content for individual users.
    * **Accessibility:** Making content creation tools available to a wider audience.
    
    **Challenges of GenAI:**
    
    * **Ethical
    ________________________________________________________________________________
     concerns:** Potential misuse for misinformation or harmful content.
    * **Bias and fairness:**  Models can reflect biases present in the training data.
    * **Copyright and ownership:** Determining the ownership of generated content.
    
    Overall, GenAI is a rapidly evolving field with the potential to revolutionize how we create and consume content
    ________________________________________________________________________________
    . It offers exciting possibilities but also raises important questions about its ethical implications and future development. 
    
    ________________________________________________________________________________



```python
chatbot = dcgm.GeminiChatbot()
chatbot.chat()
```

    Welcome to GeminiChatbot! ('/q' to exit)
    
    1 Chatbot: Hello! 👋 How can I help you today? 
    
    2 Chatbot: Why don't scientists trust atoms? 
    
    Because they make up everything! 😜 
    
    3 Chatbot: Why did the scarecrow win an award? 
    
    Because he was outstanding in his field! 🌾 
    
    4 Chatbot: The first joke was: 
    
    Why don't scientists trust atoms? 
    
    Because they make up everything! 😜 
    
    chat log file: ./log/chat-log-2024-08-19_07-19-50.txt
    Chat history saved. Exiting.

