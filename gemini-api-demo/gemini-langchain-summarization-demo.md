# Summarization using Gemini + Langchain

## Overview

[Gemini](https://ai.google.dev/models/gemini) - family of generative AI models used to generate content and solve problems; used to handle both text and images as input.

[LangChain](https://www.langchain.com/) - data framework to integrate with Large Language Models (LLM) like Gemini easier for applications.

Here is demo how to create an application to summarize large documents using the Gemini API and LangChain.


## Installation


```python
!pip install --quiet langchain-core
!pip install --quiet langchain
!pip install --quiet langchain-google-genai
!pip install --quiet -U langchain-community
```


```python
from langchain import PromptTemplate
from langchain.document_loaders import WebBaseLoader
from langchain.schema import StrOutputParser
from langchain.schema.prompt_template import format_document
```

## Setup API key

Place below line to .env under current folder, 

GOOGLE_API_KEY=xxx



```python
import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
```

## Summarize text

Perform the following steps:
1. Read and parse the website data using LangChain.
2. Chain together the following:
    * A prompt for extracting the required input data from the parsed website data.
    * A prompt for summarizing the text using LangChain.
    * An LLM model (such as the Gemini model) for prompting.
3. Run the created chain to prompt the model for the summary of the website data.

### Read and parse the website data


```python
loader = WebBaseLoader("https://dreamcloud.artark.ca/build-k8s-cluster-on-hyper-v/")
docs = loader.load()
```

### Initialize the Gemini model

Use Gemini 1.5 Flash, (`gemini-1.5-flash-latest`), as it supports text summarization. 


```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")
```

### Create prompt templates

Use LangChain's [`PromptTemplate`](https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/) to generate prompts for summarizing the text.


```python
# To extract data from WebBaseLoader
doc_prompt = PromptTemplate.from_template("{page_content}")

# To query Gemini
llm_prompt_template = """Write a concise summary of the following:
"{text}"
CONCISE SUMMARY:"""
llm_prompt = PromptTemplate.from_template(llm_prompt_template)

print(llm_prompt)
```

    input_variables=['text'] template='Write a concise summary of the following:\n"{text}"\nCONCISE SUMMARY:'


### Create a Stuff documents chain

LangChain provides [Chains](https://python.langchain.com/docs/modules/chains/) for chaining together LLMs with each other or other components for complex applications, create a **Stuff documents chain** to combine all the documents, insert them into the prompt and pass that prompt to the LLM.


```python
stuff_chain = (
    # Extract data from the documents and add to the key `text`.
    {
        "text": lambda docs: "\n\n".join(
            format_document(doc, doc_prompt) for doc in docs
        )
    }
    | llm_prompt         # Prompt for Gemini
    | llm                # Gemini API function
    | StrOutputParser()  # output parser
)
```

### Prompt the model


```python
from IPython.display import display
from IPython.display import Markdown
import textwrap

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
```


```python
to_markdown(stuff_chain.invoke(docs))
```




> This article provides a comprehensive guide on building a Kubernetes cluster on Hyper-V using Vagrant. It addresses the challenges of setting up static IP addresses for Hyper-V VMs and configuring networks, offering solutions using PowerShell scripts and Vagrantfile modifications. 
> 
> The author demonstrates how to create a 2-node Kubernetes cluster with static IPs, install Docker and Kubernetes, and automate the process using Vagrant. They also introduce a set of scripts for setting up Kubernetes clusters on various platforms, including physical Linux, Linux VMs, and WSL2. 
> 
> The article concludes by highlighting the benefits of using this method for local Kubernetes lab environments for testing and educational purposes. 




## Conclusion

In this demo, we've explored how to use Gemini and LangChain to build an application for summarizing large documents. The process involved reading and parsing website data, creating a chain of prompts and models, and using the Gemini API to generate concise summaries. The combination of Gemini's generative AI capabilities with LangChain's framework simplifies the integration and handling of complex data, making it easier to extract meaningful insights from extensive text sources.

This approach is particularly useful for efficiently condensing large amounts of information into concise summaries, aiding in quick comprehension and decision-making. Whether for research, business, or educational purposes, the techniques demonstrated here provide a powerful toolset for leveraging AI to streamline information processing and enhance content accessibility.




```python

```
