# Gemini pdf demo

## Setup


```python
!pip install -Uq google-generativeai
```


```python
import google.generativeai as genai
import os
import pathlib
import tqdm

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
```

## PDF tool to display page

PDF processing tools, no need to use the api, just to display a screenshot of a page.


```python
!sudo apt install poppler-utils
```

## Download PDF


```python
if not pathlib.Path('test.pdf').exists():
  !curl -o test.pdf https://storage.googleapis.com/cloud-samples-data/generative-ai/pdf/2403.05530.pdf

!ls -ltr |grep test.pdf
```

    -rwxrwxrwx 1 oldhorse oldhorse   7228817 Jul 28 15:25 test.pdf


Look at one of the pages:


```python
!pdftoppm test.pdf -f 3 -l 5 page-image -jpeg
!ls | grep page-image
```

    page-image-01.jpg
    page-image-03.jpg
    page-image-04.jpg
    page-image-05.jpg



```python
import PIL.Image
```


```python
img = PIL.Image.open(f"page-image-03.jpg")
img.thumbnail([800, 800])
img
```




    
![png](output_12_1.png)
    



## Upload the file to the API


```python
pdffile = genai.upload_file('test.pdf')
```


```python
model = genai.GenerativeModel(model_name='gemini-1.5-flash')
```

The pages of the PDF file are each passed to the model as a screenshot of the page plus the text extracted by OCR.


```python
model.count_tokens([pdffile, "Can you summarize this file for me?"])
```




    total_tokens: 78591




```python
response = model.generate_content(
    [pdffile, '\n\nCan you summarize this file as a bulleted list?']
)
```


```python
from IPython.display import Markdown
Markdown(response.text)
```




Here is a summary of the file as a bulleted list:

- **Gemini 1.5 Pro** is a highly compute-efficient multimodal mixture-of-experts model that is capable of recalling and reasoning over fine-grained information from millions of tokens of context, including multiple long documents and hours of video and audio. 
- Gemini 1.5 Pro achieves near-perfect recall on long-context retrieval tasks across modalities, improves the state-of-the-art in long-document QA, long-video QA and long-context ASR, and matches or surpasses Gemini 1.0 Ultra's state-of-the-art performance across a broad set of benchmarks.
- Gemini 1.5 Pro greatly surpasses Gemini 1.0 Pro, performing better on the vast majority of benchmarks, increasing the margin in particular for Math, Science and Reasoning, Multilinguality, Video Understanding, Image Understanding, and Code. 
- Gemini 1.5 Pro is able to handle extremely long-context tasks, such as long-document QA from 700k-word material and long-video QA from 40 to 105 minutes long videos. 
- Gemini 1.5 Pro is able to use in-context learning to translate from English to Kalamang, an extremely low-resource language with fewer than 200 speakers, solely by providing a grammar manual in its context at inference time.
- Gemini 1.5 Pro is able to perform well on various tasks like code generation, math and science reasoning, instruction following, and image and video understanding.
- Gemini 1.5 Pro is consistently performing better than previous models, and is able to achieve results comparable to human performance on some tasks, such as translating a new language from a single book.
- Gemini 1.5 Pro is trained and evaluated in a responsible manner, and Google has put in place several mitigation efforts to address potential risks and harms associated with the model.
- The long-context capabilities of Gemini 1.5 Pro are still under development, and there is a need for new and improved benchmarks that can adequately test the model's abilities. 





```python

```
