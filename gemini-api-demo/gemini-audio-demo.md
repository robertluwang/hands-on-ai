# Gemini audio demo

- Describe, summarize, or answer questions about the audio content
- Provide a transcription of the audio
- Provide answers or a transcription about a specific segment of the audio

## support audio format

- WAV - audio/wav
- MP3 - audio/mp3
- AIFF - audio/aiff
- AAC - audio/aac
- OGG Vorbis - audio/ogg
- FLAC - audio/flac

## Setup


```python
import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
```

## Upload audio file


```python
!curl -o sample.mp3 https://storage.googleapis.com/generativeai-downloads/data/State_of_the_Union_Address_30_January_1961.mp3
```

      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100 39.8M  100 39.8M    0     0  3338k      0  0:00:12  0:00:12 --:--:-- 4017k



```python
!pwd
!ls -ltr | grep mp3
```

```python
# Upload the file.
audio_file = genai.upload_file(path='sample.mp3')
audio_file
```




    genai.File({
        'name': 'files/pwckvrfdwzrz',
        'display_name': 'sample.mp3',
        'mime_type': 'audio/mpeg',
        'sha256_hash': 'MGU3ZmFmZTE5ODRhZWQyNGMxNWJlMDc4OWEzNWU2MGM1YWYwYzczNzNiOWVkOWYyNjMxMzE2NzQwYTRiOWVlNg==',
        'size_bytes': '41762063',
        'state': 'ACTIVE',
        'uri': 'https://generativelanguage.googleapis.com/v1beta/files/pwckvrfdwzrz',
        'create_time': '2024-07-28T03:57:50.457186Z',
        'expiration_time': '2024-07-30T03:57:50.444958949Z',
        'update_time': '2024-07-28T03:57:50.457186Z'})




```python
# List all uploaded files.
for file in genai.list_files():
    print(f"{file.display_name}, URI: {file.uri}")
```

    sample.mp3, URI: https://generativelanguage.googleapis.com/v1beta/files/pwckvrfdwzrz
    sample.mp3, URI: https://generativelanguage.googleapis.com/v1beta/files/6e64qsy4tbuj


## Summarize audio


```python
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

prompt = "Summarize the speech."

response = model.generate_content([prompt, audio_file])
print(response)
model.count_tokens([audio_file])
print(response.text)
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
                    "text": "This is President John F. Kennedy\u2019s State of the Union address delivered to a joint session of Congress on January 30th, 1961. The address covers the current state of the economy, international relations, and the executive branch. The president begins with an optimistic outlook and a reminder of the strength of the US, but he acknowledges the need for change in order to address the challenges ahead. The address touches upon domestic issues such as unemployment, housing, education, and health care, and it emphasizes the importance of taking action to address these problems. Kennedy then shifts focus to international affairs, highlighting the Cold War, the situation in Laos and the Congo, and the need for a strong national defense. He emphasizes the importance of working with allies and promoting economic development, particularly in Latin America. The president concludes with a call for dedication and perseverance, reminding the nation that the challenges ahead require the collective effort of all citizens. He concludes with a reference to the words of a great president, emphasizing the importance of working towards a brighter future. "
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
            "prompt_token_count": 83558,
            "candidates_token_count": 212,
            "total_token_count": 83770
          }
        }),
    )
    This is President John F. Kennedy’s State of the Union address delivered to a joint session of Congress on January 30th, 1961. The address covers the current state of the economy, international relations, and the executive branch. The president begins with an optimistic outlook and a reminder of the strength of the US, but he acknowledges the need for change in order to address the challenges ahead. The address touches upon domestic issues such as unemployment, housing, education, and health care, and it emphasizes the importance of taking action to address these problems. Kennedy then shifts focus to international affairs, highlighting the Cold War, the situation in Laos and the Congo, and the need for a strong national defense. He emphasizes the importance of working with allies and promoting economic development, particularly in Latin America. The president concludes with a call for dedication and perseverance, reminding the nation that the challenges ahead require the collective effort of all citizens. He concludes with a reference to the words of a great president, emphasizing the importance of working towards a brighter future. 


## Get a transcript of the audio file
https://github.com/google-gemini/generative-ai-python/issues/336 seems known issue


```python
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

prompt = "Generate a transcript of the speech."

response = model.generate_content([prompt, audio_file])
print(response)
print(response.text)
```


```python
prompt = "Provide a transcript of the speech from 02:30 to 03:29."
response = model.generate_content([prompt, audio_file])
print(response.text)
```

## Manage uploaded file


```python
# List all uploaded files.
for file in genai.list_files():
    print(f"{file.display_name}, URI: {file.uri}")
```


```python
for file in genai.list_files():
    genai.delete_file(file)
    print(f'Deleted file {file.uri}')
```

## audio file as inline data


```python
# Download an audio file from a remote server to a cache directory on your local host.
!curl -o samplesmall.mp3 https://storage.googleapis.com/generativeai-downloads/data/Apollo-11_Day-01-Highlights-10s.mp3
```


```python
import pathlib

model = genai.GenerativeModel('models/gemini-1.5-flash')

prompt = "Please summarize the audio."

response = model.generate_content([
    prompt,
    {
        "mime_type": "audio/mp3",
        "data": pathlib.Path('samplesmall.mp3').read_bytes()
    }
])

print(response.text)
```
