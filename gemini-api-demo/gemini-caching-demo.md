# Gemini Caching demo


```python
!pip install -qU 'google-generativeai'
```


```python
import google.generativeai as genai
from google.generativeai import caching
```

## Setup API key


```python
import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
```

## Upload a file

When ask a number of questions of the same document, context caching will save time, more efficient by avoiding to pass the same tokens for each new request.



```python
!wget -q https://storage.googleapis.com/generativeai-downloads/data/a11.txt
!head a11.txt
```

    INTRODUCTION
    
    This is the transcription of the Technical Air-to-Ground Voice Transmission (GOSS NET 1) from the Apollo 11 mission.
    
    Communicators in the text may be identified according to the following list.
    
    Spacecraft:
    CDR	Commander	Neil A. Armstrong
    CMP	Command module pilot   	Michael Collins
    LMP	Lunar module pilot	Edwin E. ALdrin, Jr.



```python
document = genai.upload_file(path="a11.txt")
document
```




    genai.File({
        'name': 'files/rdiqeej4078v',
        'display_name': 'a11.txt',
        'mime_type': 'text/plain',
        'sha256_hash': 'MGQyN2JkYzNlMDU5ZDIwNjI3ZWQ4MjhhMzExMzhiMjk0ZDcwYjk5NmIwZjZjOGFkMWI1MzAyNmQyMDgzOTk1MQ==',
        'size_bytes': '847790',
        'state': 'ACTIVE',
        'uri': 'https://generativelanguage.googleapis.com/v1beta/files/rdiqeej4078v',
        'create_time': '2024-07-28T15:28:26.854726Z',
        'expiration_time': '2024-07-30T15:28:26.842745036Z',
        'update_time': '2024-07-28T15:28:26.854726Z'})



## Cache the prompt

Let's create cached content prompt including:
- system_instruction
- file


```python
# Note that caching requires a frozen model, e.g. one with a `-001` version suffix.
model_name = "gemini-1.5-flash-001"

apollo_cache = caching.CachedContent.create(
    model=model_name,
    system_instruction="You are an expert at analyzing transcripts.",
    contents=[document],
)

apollo_cache
```




    CachedContent(
        name='cachedContents/4mlthvd4u5wz',
        model='models/gemini-1.5-flash-001',
        display_name='',
        usage_metadata={
            'total_token_count': 323383,
        },
        create_time=2024-07-28 15:32:30.321933+00:00,
        update_time=2024-07-28 15:32:30.321933+00:00,
        expire_time=2024-07-28 16:32:30.154499+00:00
    )



## Manage the cache expiry

update the expiry time to keep it alive while you need it.


```python
import datetime

apollo_cache.update(ttl=datetime.timedelta(hours=1))
apollo_cache
```




    CachedContent(
        name='cachedContents/4mlthvd4u5wz',
        model='models/gemini-1.5-flash-001',
        display_name='',
        usage_metadata={
            'total_token_count': 323383,
        },
        create_time=2024-07-28 15:32:30.321933+00:00,
        update_time=2024-07-28 15:33:13.193517+00:00,
        expire_time=2024-07-28 16:33:13.181690+00:00
    )



## Use the cache for generation


```python
apollo_model = genai.GenerativeModel.from_cached_content(cached_content=apollo_cache)

response = apollo_model.generate_content("Find a lighthearted moment from this transcript")
print(response.text)
```

    One lighthearted moment occurs on **Tape 2/5, Page 13** around **01:54:38**. 
    
    After Mission Control relays that the spacecraft has a 99% probability of a successful landing, CMP Mike Collins responds with:
    
    "**Roger. We like those 99 numbers. Thank you.**"
    
    This demonstrates a bit of lightheartedness between the crew and Mission Control, as Collins jokes about enjoying the odds being in their favor. 
    


You can inspect token usage through `usage_metadata`. Note that the cached prompt tokens are included in `prompt_token_count`, but excluded from the `total_token_count`.


```python
response.usage_metadata
```




    prompt_token_count: 323392
    cached_content_token_count: 323383
    candidates_token_count: 101
    total_token_count: 323493



You can ask new questions of the model, and the cache is reused.


```python
chat = apollo_model.start_chat()
response = chat.send_message("Give me a quote from the most important part of the transcript.")
print(response.text)
```

    The most important part of the transcript is the landing of the Eagle. A quote from that section is:
    
    **"Houston, Tranquility Base here. The Eagle has landed."** 
    



```python
response = chat.send_message("What was recounted after that?")
print(response.text)
```

    After Neil Armstrong's iconic declaration, "Houston, Tranquility Base here. The Eagle has landed,"  the following events were recounted:
    
    * **Mission Control's response:**  "Roger, Tranquility. We copy you on the ground. You got a bunch of guys about to turn blue. We're breathing again. Thanks a lot." 
    
    * **Armstrong's confirmation:** "Thank you."
    
    * **Aldrin's confirmation:** "Very smooth touchdown."
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic."
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic."
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger. We have it." 
    
    * **Collins's response from Columbia:** "Fantastic." 
    
    * **Aldrin's actions:** "Engine STOP RESET. ... copy NOUN 60, NOUN 43. Over."
    
    * **Mission Control's acknowledgement:** "Roger



```python
response.usage_metadata
```




    prompt_token_count: 323455
    candidates_token_count: 164
    total_token_count: 236
    cached_content_token_count: 323383



## Counting tokens


```python
apollo_model.count_tokens("How many people are involved in this transcript?")
```




    total_tokens: 9



## Delete the cache

A cache object:
- deleted automatically when it expires
- also explicitly deleted


```python
print(apollo_cache.name)
apollo_cache.delete()
```

    cachedContents/4mlthvd4u5wz

