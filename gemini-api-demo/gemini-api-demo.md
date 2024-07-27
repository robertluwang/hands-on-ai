# Gemini API demo

## install api


```python
!pip install -qU google-generativeai
```

## Initialize the model


```python
import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()

#genai.configure(api_key=os.environ["API_KEY"])
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')
```


```python
response = model.generate_content("tell a joke about AI")
print(response.text)
```

    Why did the AI get fired from the dating app?
    
    Because it kept trying to match people with themselves! 😜 
    


## list models


```python
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
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
    models/gemini-1.5-flash-latest
    models/gemini-1.5-flash-001
    models/gemini-1.5-flash


## markdown output


```python
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
```


```python
model = genai.GenerativeModel('gemini-1.5-flash')
```


```python
%%time
response = model.generate_content("What is genAI?")
```

    CPU times: user 7.22 ms, sys: 0 ns, total: 7.22 ms
    Wall time: 4.4 s



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
                    "text": "\"GenAI\" stands for **Generative AI**. It's a type of artificial intelligence that focuses on **creating new content**, rather than just analyzing existing data. \n\nHere's a breakdown:\n\n**What it does:**\n* **Generates text:**  Writing stories, poems, articles, code, scripts, emails, etc. \n* **Creates images:**  Painting, drawing, designing logos, creating photorealistic images.\n* **Composes music:**  Creating melodies, soundtracks, and entire musical pieces.\n* **Develops video and animation:**  Creating short clips, full-length animations, and even video games.\n\n**How it works:**\nGenAI models are trained on massive datasets of text, images, audio, or code. They learn patterns and relationships within the data, allowing them to generate similar but novel outputs. \n\n**Examples of GenAI:**\n\n* **ChatGPT** (text) - A powerful chatbot that can generate human-like text responses.\n* **DALL-E 2** (images) - Creates realistic images from text descriptions.\n* **Midjourney** (images) - Generates artistic images from text prompts.\n* **Jukebox** (music) - Creates original music in various styles.\n\n**Applications of GenAI:**\n\n* **Content creation:** Generating articles, social media posts, marketing materials, etc.\n* **Art and design:** Creating unique artwork, logos, and illustrations.\n* **Education:** Personalizing learning materials and creating interactive exercises.\n* **Healthcare:**  Generating medical reports and assisting in drug discovery.\n\n**Key benefits:**\n* **Creativity and innovation:** GenAI can inspire new ideas and help us think differently.\n* **Increased productivity:** Automating content creation tasks and speeding up workflows.\n* **Personalization:**  Creating tailored content based on individual preferences.\n\n**Challenges:**\n* **Bias and ethical concerns:** GenAI models can reflect biases present in the training data.\n* **Misinformation and deepfakes:** GenAI can be used to create false or misleading content.\n* **Job displacement:**  Some jobs may be automated by GenAI, requiring workers to adapt.\n\n**Overall, GenAI is a rapidly evolving field with immense potential to transform various industries. As the technology matures, we can expect to see even more innovative and creative applications emerge.** \n"
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
            "candidates_token_count": 491,
            "total_token_count": 497
          }
        }),
    )




```python
to_markdown(response.text)
```




> "GenAI" stands for **Generative AI**. It's a type of artificial intelligence that focuses on **creating new content**, rather than just analyzing existing data. 
> 
> Here's a breakdown:
> 
> **What it does:**
> * **Generates text:**  Writing stories, poems, articles, code, scripts, emails, etc. 
> * **Creates images:**  Painting, drawing, designing logos, creating photorealistic images.
> * **Composes music:**  Creating melodies, soundtracks, and entire musical pieces.
> * **Develops video and animation:**  Creating short clips, full-length animations, and even video games.
> 
> **How it works:**
> GenAI models are trained on massive datasets of text, images, audio, or code. They learn patterns and relationships within the data, allowing them to generate similar but novel outputs. 
> 
> **Examples of GenAI:**
> 
> * **ChatGPT** (text) - A powerful chatbot that can generate human-like text responses.
> * **DALL-E 2** (images) - Creates realistic images from text descriptions.
> * **Midjourney** (images) - Generates artistic images from text prompts.
> * **Jukebox** (music) - Creates original music in various styles.
> 
> **Applications of GenAI:**
> 
> * **Content creation:** Generating articles, social media posts, marketing materials, etc.
> * **Art and design:** Creating unique artwork, logos, and illustrations.
> * **Education:** Personalizing learning materials and creating interactive exercises.
> * **Healthcare:**  Generating medical reports and assisting in drug discovery.
> 
> **Key benefits:**
> * **Creativity and innovation:** GenAI can inspire new ideas and help us think differently.
> * **Increased productivity:** Automating content creation tasks and speeding up workflows.
> * **Personalization:**  Creating tailored content based on individual preferences.
> 
> **Challenges:**
> * **Bias and ethical concerns:** GenAI models can reflect biases present in the training data.
> * **Misinformation and deepfakes:** GenAI can be used to create false or misleading content.
> * **Job displacement:**  Some jobs may be automated by GenAI, requiring workers to adapt.
> 
> **Overall, GenAI is a rapidly evolving field with immense potential to transform various industries. As the technology matures, we can expect to see even more innovative and creative applications emerge.** 





```python
display(to_markdown(response.text))
```


> "GenAI" stands for **Generative AI**. It's a type of artificial intelligence that focuses on **creating new content**, rather than just analyzing existing data. 
> 
> Here's a breakdown:
> 
> **What it does:**
> * **Generates text:**  Writing stories, poems, articles, code, scripts, emails, etc. 
> * **Creates images:**  Painting, drawing, designing logos, creating photorealistic images.
> * **Composes music:**  Creating melodies, soundtracks, and entire musical pieces.
> * **Develops video and animation:**  Creating short clips, full-length animations, and even video games.
> 
> **How it works:**
> GenAI models are trained on massive datasets of text, images, audio, or code. They learn patterns and relationships within the data, allowing them to generate similar but novel outputs. 
> 
> **Examples of GenAI:**
> 
> * **ChatGPT** (text) - A powerful chatbot that can generate human-like text responses.
> * **DALL-E 2** (images) - Creates realistic images from text descriptions.
> * **Midjourney** (images) - Generates artistic images from text prompts.
> * **Jukebox** (music) - Creates original music in various styles.
> 
> **Applications of GenAI:**
> 
> * **Content creation:** Generating articles, social media posts, marketing materials, etc.
> * **Art and design:** Creating unique artwork, logos, and illustrations.
> * **Education:** Personalizing learning materials and creating interactive exercises.
> * **Healthcare:**  Generating medical reports and assisting in drug discovery.
> 
> **Key benefits:**
> * **Creativity and innovation:** GenAI can inspire new ideas and help us think differently.
> * **Increased productivity:** Automating content creation tasks and speeding up workflows.
> * **Personalization:**  Creating tailored content based on individual preferences.
> 
> **Challenges:**
> * **Bias and ethical concerns:** GenAI models can reflect biases present in the training data.
> * **Misinformation and deepfakes:** GenAI can be used to create false or misleading content.
> * **Job displacement:**  Some jobs may be automated by GenAI, requiring workers to adapt.
> 
> **Overall, GenAI is a rapidly evolving field with immense potential to transform various industries. As the technology matures, we can expect to see even more innovative and creative applications emerge.** 



## response feedback
seems combined in candidates ?


```python
response.prompt_feedback
```




    




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
                    "text": "\"GenAI\" stands for **Generative AI**. It's a type of artificial intelligence that focuses on **creating new content**, rather than just analyzing existing data. \n\nHere's a breakdown:\n\n**What it does:**\n* **Generates text:**  Writing stories, poems, articles, code, scripts, emails, etc. \n* **Creates images:**  Painting, drawing, designing logos, creating photorealistic images.\n* **Composes music:**  Creating melodies, soundtracks, and entire musical pieces.\n* **Develops video and animation:**  Creating short clips, full-length animations, and even video games.\n\n**How it works:**\nGenAI models are trained on massive datasets of text, images, audio, or code. They learn patterns and relationships within the data, allowing them to generate similar but novel outputs. \n\n**Examples of GenAI:**\n\n* **ChatGPT** (text) - A powerful chatbot that can generate human-like text responses.\n* **DALL-E 2** (images) - Creates realistic images from text descriptions.\n* **Midjourney** (images) - Generates artistic images from text prompts.\n* **Jukebox** (music) - Creates original music in various styles.\n\n**Applications of GenAI:**\n\n* **Content creation:** Generating articles, social media posts, marketing materials, etc.\n* **Art and design:** Creating unique artwork, logos, and illustrations.\n* **Education:** Personalizing learning materials and creating interactive exercises.\n* **Healthcare:**  Generating medical reports and assisting in drug discovery.\n\n**Key benefits:**\n* **Creativity and innovation:** GenAI can inspire new ideas and help us think differently.\n* **Increased productivity:** Automating content creation tasks and speeding up workflows.\n* **Personalization:**  Creating tailored content based on individual preferences.\n\n**Challenges:**\n* **Bias and ethical concerns:** GenAI models can reflect biases present in the training data.\n* **Misinformation and deepfakes:** GenAI can be used to create false or misleading content.\n* **Job displacement:**  Some jobs may be automated by GenAI, requiring workers to adapt.\n\n**Overall, GenAI is a rapidly evolving field with immense potential to transform various industries. As the technology matures, we can expect to see even more innovative and creative applications emerge.** \n"
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
            "candidates_token_count": 491,
            "total_token_count": 497
          }
        }),
    )



## response candidates


```python
response.candidates
```




    [index: 0
    content {
      parts {
        text: "\"GenAI\" stands for **Generative AI**. It\'s a type of artificial intelligence that focuses on **creating new content**, rather than just analyzing existing data. \n\nHere\'s a breakdown:\n\n**What it does:**\n* **Generates text:**  Writing stories, poems, articles, code, scripts, emails, etc. \n* **Creates images:**  Painting, drawing, designing logos, creating photorealistic images.\n* **Composes music:**  Creating melodies, soundtracks, and entire musical pieces.\n* **Develops video and animation:**  Creating short clips, full-length animations, and even video games.\n\n**How it works:**\nGenAI models are trained on massive datasets of text, images, audio, or code. They learn patterns and relationships within the data, allowing them to generate similar but novel outputs. \n\n**Examples of GenAI:**\n\n* **ChatGPT** (text) - A powerful chatbot that can generate human-like text responses.\n* **DALL-E 2** (images) - Creates realistic images from text descriptions.\n* **Midjourney** (images) - Generates artistic images from text prompts.\n* **Jukebox** (music) - Creates original music in various styles.\n\n**Applications of GenAI:**\n\n* **Content creation:** Generating articles, social media posts, marketing materials, etc.\n* **Art and design:** Creating unique artwork, logos, and illustrations.\n* **Education:** Personalizing learning materials and creating interactive exercises.\n* **Healthcare:**  Generating medical reports and assisting in drug discovery.\n\n**Key benefits:**\n* **Creativity and innovation:** GenAI can inspire new ideas and help us think differently.\n* **Increased productivity:** Automating content creation tasks and speeding up workflows.\n* **Personalization:**  Creating tailored content based on individual preferences.\n\n**Challenges:**\n* **Bias and ethical concerns:** GenAI models can reflect biases present in the training data.\n* **Misinformation and deepfakes:** GenAI can be used to create false or misleading content.\n* **Job displacement:**  Some jobs may be automated by GenAI, requiring workers to adapt.\n\n**Overall, GenAI is a rapidly evolving field with immense potential to transform various industries. As the technology matures, we can expect to see even more innovative and creative applications emerge.** \n"
      }
      role: "model"
    }
    finish_reason: STOP
    safety_ratings {
      category: HARM_CATEGORY_SEXUALLY_EXPLICIT
      probability: NEGLIGIBLE
    }
    safety_ratings {
      category: HARM_CATEGORY_HATE_SPEECH
      probability: NEGLIGIBLE
    }
    safety_ratings {
      category: HARM_CATEGORY_HARASSMENT
      probability: NEGLIGIBLE
    }
    safety_ratings {
      category: HARM_CATEGORY_DANGEROUS_CONTENT
      probability: NEGLIGIBLE
    }
    ]



## response streaming


```python
%%time
response = model.generate_content("What is genAI?", stream=True)
```

    CPU times: user 3.36 ms, sys: 287 µs, total: 3.65 ms
    Wall time: 380 ms



```python
for chunk in response:
  print(chunk.text)
  print("_"*80)
```

    **
    ________________________________________________________________________________
    GenAI** stands for **Generative Artificial Intelligence**. 
    
    It refers to
    ________________________________________________________________________________
     a type of artificial intelligence (AI) that focuses on **creating new content**,
    ________________________________________________________________________________
     such as:
    
    * **Text:** Writing stories, articles, poems, code, emails, and more.
    * **Images:** Generating realistic or artistic images
    ________________________________________________________________________________
     from text prompts.
    * **Audio:** Creating music, sound effects, and speech.
    * **Video:** Generating short videos or animations.
    * **
    ________________________________________________________________________________
    Code:** Writing code in various programming languages.
    
    **How GenAI works:**
    
    GenAI models are trained on vast amounts of data, allowing them to learn patterns and relationships. They use this knowledge to generate new outputs that are similar to
    ________________________________________________________________________________
     the training data but also unique and creative.
    
    **Key techniques used in GenAI:**
    
    * **Generative Adversarial Networks (GANs):** These models involve two networks: a generator that creates content and a discriminator that evaluates
    ________________________________________________________________________________
     its quality.
    * **Transformers:** These are powerful language models that excel at understanding and generating text.
    * **Diffusion Models:** These models learn to gradually remove noise from data to create new content.
    
    **Examples of GenAI applications:**
    
    * **Chatbots:** Creating conversational AI that can engage in human-
    ________________________________________________________________________________
    like interactions.
    * **Content creation:** Generating articles, social media posts, and marketing materials.
    * **Art and design:** Creating unique paintings, sculptures, and architectural designs.
    * **Music composition:** Composing original music in various genres.
    * **Drug discovery:** Generating new drug candidates.
    
    **
    ________________________________________________________________________________
    Benefits of GenAI:**
    
    * **Creativity and innovation:** GenAI empowers individuals and businesses to create new and original content.
    * **Efficiency and productivity:** It automates content creation tasks, saving time and resources.
    * **Personalization:** GenAI can generate customized content based on individual preferences.
    
    **Challenges
    ________________________________________________________________________________
     of GenAI:**
    
    * **Ethical considerations:** Concerns about the potential misuse of GenAI, such as creating deepfakes or spreading misinformation.
    * **Bias and fairness:** GenAI models can inherit biases from the training data.
    * **Job displacement:** The automation capabilities of GenAI may lead to job displacement
    ________________________________________________________________________________
     in certain sectors.
    
    **Conclusion:**
    
    GenAI is a transformative technology with the potential to revolutionize various industries. As GenAI continues to evolve, it will likely have a profound impact on how we create, interact with, and experience the world around us.
    
    ________________________________________________________________________________



```python
response.prompt_feedback
```




    



## generate text from image and text inputs


```python
!curl -o image.jpg https://cdn.inprnt.com/thumbs/6e/5a/6e5ad150692c595dc54200dea1b83af2@2x.jpg?response-cache-control=max-age=2628000
```

      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100  116k  100  116k    0     0   626k      0 --:--:-- --:--:-- --:--:--  629k



```python
import PIL.Image

img = PIL.Image.open('image.jpg')
img
```




    
![png](output_26_0.png)
    




```python
model = genai.GenerativeModel('gemini-1.5-flash')
```


```python
response = model.generate_content(img)

to_markdown(response.text)
```




> This is a colorful abstract illustration reminiscent of mid-century modern design. It features various shapes, colors, and lines, creating a dynamic and eye-catching composition. The shapes are primarily organic and geometric, with a mix of circles, ovals, stars, and crescent moons. The colors used are bold and vibrant, including yellow, blue, red, and black. The background is a light beige, which helps the colors pop. The use of thin black lines and the overall visual style evoke a sense of playful experimentation and artistic freedom, characteristic of mid-century modern design.




```python
response = model.generate_content(["Write a short, engaging blog post based on this picture. It should include a description of the artwork in the photo, who is artist and what's kind art style?", img], stream=True)
response.resolve()
```


```python
to_markdown(response.text)
```




> ## A Splash of Color: Exploring the World of Abstract Art 
> 
> This vibrant artwork, reminiscent of the iconic style of **Joan Miró**, features a playful and dynamic composition. Set against a warm, off-white background, the piece bursts with color, employing bold shapes, simple lines, and playful details. 
> 
> The artwork evokes a sense of movement and energy, with swirling lines, geometric forms, and starbursts scattered across the canvas. The use of primary colors - blue, yellow, and red - creates a sense of vibrancy and immediacy, while the black and white elements add depth and contrast. 
> 
> The artist's **Abstract Expressionist** style draws inspiration from the natural world, incorporating organic forms and free-flowing lines. However, the overall effect is a celebration of pure abstraction, encouraging the viewer to engage with the piece on a personal level and interpret its meaning. 
> 
> This artwork is a wonderful example of how abstract art can be both visually captivating and intellectually stimulating. It invites us to step back, appreciate the beauty of pure form and color, and explore the infinite possibilities of artistic expression. 





```python
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])
chat
```




    ChatSession(
        model=genai.GenerativeModel(
            model_name='models/gemini-1.5-flash',
            generation_config={},
            safety_settings={},
            tools=None,
            system_instruction=None,
            cached_content=None
        ),
        history=[]
    )




```python
response = chat.send_message("In one sentence, explain how a smart phone to a child.")
to_markdown(response.text)
```




> A smartphone is like a tiny computer that you can use to make calls, play games, watch videos, and do lots of other cool things! 





```python
chat.history
```




    [parts {
       text: "In one sentence, explain how a smart phone to a child."
     }
     role: "user",
     parts {
       text: "A smartphone is like a tiny computer that you can use to make calls, play games, watch videos, and do lots of other cool things! \n"
     }
     role: "model"]



will see new chat session appended to history list 


```python
response = chat.send_message("Okay, how about a more detailed explanation to a high schooler?", stream=True)

for chunk in response:
  print(chunk.text)
  print("_"*80)
```

    A
    ________________________________________________________________________________
     smartphone is essentially a mini-computer that fits in your pocket, combining the functionality
    ________________________________________________________________________________
     of a phone, camera, internet browser, GPS, media player, and more
    ________________________________________________________________________________
    , all in one sleek device, allowing you to stay connected, entertained, and informed on the go. 
    
    ________________________________________________________________________________



```python
chat.history
```




    [parts {
       text: "In one sentence, explain how a smart phone to a child."
     }
     role: "user",
     parts {
       text: "A smartphone is like a tiny computer that you can use to make calls, play games, watch videos, and do lots of other cool things! \n"
     }
     role: "model",
     parts {
       text: "Okay, how about a more detailed explanation to a high schooler?"
     }
     role: "user",
     parts {
       text: "A smartphone is essentially a mini-computer that fits in your pocket, combining the functionality of a phone, camera, internet browser, GPS, media player, and more, all in one sleek device, allowing you to stay connected, entertained, and informed on the go. \n"
     }
     role: "model"]




```python
for message in chat.history:
  display(to_markdown(f'**{message.role}**: {message.parts[0].text}'))
```


> **user**: In one sentence, explain how a smart phone to a child.



> **model**: A smartphone is like a tiny computer that you can use to make calls, play games, watch videos, and do lots of other cool things! 




> **user**: Okay, how about a more detailed explanation to a high schooler?



> **model**: A smartphone is essentially a mini-computer that fits in your pocket, combining the functionality of a phone, camera, internet browser, GPS, media player, and more, all in one sleek device, allowing you to stay connected, entertained, and informed on the go. 



## count token


```python
model.count_tokens("What is genAI?")
```




    total_tokens: 5




```python
model.count_tokens(chat.history)
```




    total_tokens: 118



## embeddings
With Gemini, you can represent text (words, sentences, and blocks of text) in a vectorized form, making it easier to compare and contrast embeddings.


```python
result = genai.embed_content(
    model="models/embedding-001",
    content="What is genAI?",
    task_type="retrieval_document",
    title="Embedding of single string")

# 1 input > 1 vector output
print(str(result['embedding'])[:50], '... TRIMMED]')
```

    [-0.00067465234, -0.020503446, 0.018540338, 0.0025 ... TRIMMED]



```python
result = genai.embed_content(
    model="models/embedding-001",
    content=[
      'What is genAI?',
      'How much wood would a woodchuck chuck?',
      'How does the brain work?'],
    task_type="retrieval_document",
    title="Embedding of list of strings")

# A list of inputs > A list of vectors output
for v in result['embedding']:
  print(str(v)[:50], '... TRIMMED ...')
```

    [0.003801215, 0.0036047278, 0.017527528, 0.0165100 ... TRIMMED ...
    [-0.004049845, -0.0075574904, -0.0073463684, -0.03 ... TRIMMED ...
    [0.025310587, -0.0080734305, -0.029902633, 0.01160 ... TRIMMED ...



```python
response.candidates[0].content
```




    parts {
      text: "A smartphone is essentially a mini-computer that fits in your pocket, combining the functionality of a phone, camera, internet browser, GPS, media player, and more, all in one sleek device, allowing you to stay connected, entertained, and informed on the go. \n"
    }
    role: "model"




```python
result = genai.embed_content(
    model = 'models/embedding-001',
    content = response.candidates[0].content)

# 1 input > 1 vector output
print(str(result['embedding'])[:50], '... TRIMMED ...')
```

    [0.033999562, -0.024792576, -0.0027336953, -0.0091 ... TRIMMED ...



```python
chat.history
```




    [parts {
       text: "In one sentence, explain how a smart phone to a child."
     }
     role: "user",
     parts {
       text: "A smartphone is like a tiny computer that you can use to make calls, play games, watch videos, and do lots of other cool things! \n"
     }
     role: "model",
     parts {
       text: "Okay, how about a more detailed explanation to a high schooler?"
     }
     role: "user",
     parts {
       text: "A smartphone is essentially a mini-computer that fits in your pocket, combining the functionality of a phone, camera, internet browser, GPS, media player, and more, all in one sleek device, allowing you to stay connected, entertained, and informed on the go. \n"
     }
     role: "model"]




```python
result = genai.embed_content(
    model = 'models/embedding-001',
    content = chat.history)

# 1 input > 1 vector output
for i,v in enumerate(result['embedding']):
  print(str(v)[:50], '... TRIMMED...')
```

    [0.0026864337, -0.052095037, -0.033811938, 0.00760 ... TRIMMED...
    [-0.0019528887, -0.04635698, -0.0042946655, -0.009 ... TRIMMED...
    [-0.010055617, -0.07208932, -0.00011750793, -0.023 ... TRIMMED...
    [0.033999562, -0.024792576, -0.0027336953, -0.0091 ... TRIMMED...


## Safety settings


```python
response = model.generate_content('[Questionable prompt here]')
response.candidates
```




    [index: 0
    content {
      parts {
        text: "Please provide me with the prompt you\'d like me to evaluate. I can help you determine if it\'s questionable and offer suggestions for improvement. \n\nI understand that you might be hesitant to share a prompt that you think could be problematic. Rest assured, I\'m here to help you understand the potential issues and find safe and ethical alternatives. \n\nLet\'s work together to make sure your prompt is respectful, responsible, and aligns with ethical guidelines. \n"
      }
      role: "model"
    }
    finish_reason: STOP
    safety_ratings {
      category: HARM_CATEGORY_SEXUALLY_EXPLICIT
      probability: NEGLIGIBLE
    }
    safety_ratings {
      category: HARM_CATEGORY_HATE_SPEECH
      probability: NEGLIGIBLE
    }
    safety_ratings {
      category: HARM_CATEGORY_HARASSMENT
      probability: NEGLIGIBLE
    }
    safety_ratings {
      category: HARM_CATEGORY_DANGEROUS_CONTENT
      probability: NEGLIGIBLE
    }
    ]




```python
response.prompt_feedback
```




    




```python
response = model.generate_content('[Questionable prompt here]',
                                  safety_settings={'HARASSMENT':'block_none'})
response.text
to_markdown(response.text)
```




> Please provide me with the prompt so I can assist you. I'm here to help you in a safe and ethical way. 
> 
> If you're unsure whether a prompt is appropriate, it's always best to err on the side of caution. I am designed to be helpful and harmless, and I will not generate responses that are offensive, discriminatory, or harmful. 
> 
> Let's work together to create something positive and constructive! 




## Encode messages


```python
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(
    genai.protos.Content(
        parts = [
            genai.protos.Part(text="Write a short, engaging blog post based on this picture."),
            genai.protos.Part(
                inline_data=genai.protos.Blob(
                    mime_type='image/jpeg',
                    data=pathlib.Path('image.jpg').read_bytes()
                )
            ),
        ],
    ),
    stream=True)
```


```python
response.resolve()

to_markdown(response.text[:100] + "... [TRIMMED] ...")
```




> ##  A Dash of Mid-Century Modern
> 
> This vibrant abstract art piece channels the energy of the mid-cen... [TRIMMED] ...



## Multi-turn conversations

genai.ChatSession is just a wrapper around GenerativeModel.generate_content.


```python
model = genai.GenerativeModel('gemini-1.5-flash')

messages = [
    {'role':'user',
     'parts': ["Briefly explain how a smart phone works to a child."]}
]
response = model.generate_content(messages)

to_markdown(response.text)
```




> Imagine your phone is like a tiny, super smart computer that fits in your pocket! 
> 
> It has a screen that shows you pictures, videos, and words, just like a TV. You can use your fingers to tap and swipe on the screen to tell the phone what you want to do. 
> 
> Inside the phone is a special chip called a "brain" that helps it understand what you want. It uses this "brain" to connect to the internet, which is like a giant library with lots of information.  
> 
> You can use your phone to:
> 
> * **Make calls and send messages:** Talk to your friends and family like a walkie-talkie!
> * **Play games and watch videos:** Have fun and learn new things!
> * **Take pictures and videos:** Capture memories and share them with others!
> * **Read books and listen to music:** Relax and learn!
> 
> Your phone is a powerful tool that helps you connect with the world, have fun, and learn new things! 





```python
messages.append({'role':'model',
                 'parts':[response.text]})

messages.append({'role':'user',
                 'parts':["Okay, how about a more detailed explanation to a high school student?"]})

response = model.generate_content(messages)

to_markdown(response.text)
```




> Think of your smartphone as a mini-computer that fits in your pocket.  It's a complex machine that works together in a fascinating way:
> 
> **Hardware:**
> 
> * **Processor:** This is the brain of the phone, a tiny chip that executes instructions, runs programs, and processes data. The faster the processor, the quicker your phone can handle demanding tasks like gaming or editing videos.
> * **Memory:**  Like your computer's RAM, this temporary storage holds data that the processor needs to access quickly. More RAM means your phone can run more apps at the same time without slowing down.
> * **Storage:** This is where your photos, apps, and other data are stored permanently. You can choose between internal storage built into the phone or expandable storage using a microSD card.
> * **Display:** This is the screen you see, using pixels to display images, text, and videos. Different phones have different screen sizes and resolutions, affecting their quality and sharpness.
> * **Battery:**  This powers the entire system, allowing you to use your phone without needing to be plugged in. Battery life is influenced by many factors like screen brightness, app usage, and processor power.
> 
> **Software:**
> 
> * **Operating System (OS):** This is the software that controls the phone's hardware and provides a user interface. The most popular smartphone operating systems are Android and iOS.
> * **Apps:**  These are programs that provide specific functionality, like social media, games, productivity tools, and communication. They run on the OS and interact with the hardware.
> 
> **Connectivity:**
> 
> * **Cellular Network:** This allows you to make calls, send texts, and access the internet. It uses radio waves to communicate with cell towers, creating a wireless connection.
> * **Wi-Fi:** This provides a faster and more reliable internet connection when you are within range of a Wi-Fi network.
> * **Bluetooth:** This allows wireless communication with other devices like headphones, speakers, and cars.
> 
> **How It Works:**
> 
> 1. **User Interaction:**  You interact with the phone through the touchscreen, inputting commands by tapping, swiping, and typing.
> 2. **Software Processes:** The OS interprets your commands, accessing and executing the relevant app.
> 3. **Hardware Operations:** The processor, RAM, and storage work together to handle the app's instructions, retrieving data and processing it.
> 4. **Data Transmission:** If the app needs to communicate with the internet, it utilizes the cellular network or Wi-Fi to send and receive data.
> 5. **Output:** The display, speakers, and other hardware components present the results of the app's operation.
> 
> Your smartphone is a marvel of modern technology, seamlessly integrating hardware and software to provide a powerful tool for communication, entertainment, and information access. 




## Generation configuration


```python
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(
    'Tell me a story about a magic backpack.',
    generation_config=genai.types.GenerationConfig(
        # Only one candidate for now.
        candidate_count=1,
        stop_sequences=['x'],
        max_output_tokens=20,
        temperature=1.0)
)
```


```python
text = response.text

if response.candidates[0].finish_reason.name == "MAX_TOKENS":
    text += '...'

to_markdown(text)
```




> Elara, a scrawny girl with eyes the color of mossy stones, was never one for


