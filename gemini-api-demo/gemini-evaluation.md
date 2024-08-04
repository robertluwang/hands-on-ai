# Build an essay evaluation using Gemini Flash

## Overview
Gemini API used for various forms of evaluation:
- Providing feedback based on selected criteria
- Comparing multiple texts
- Assigning grades or confidence scores
- Identifying weak areas

Here is demo of using the LLM to enhance text quality through feedback and grading.

## Installation


```python
!pip install -U -q google-generativeai
```


```python
import google.generativeai as genai

from IPython.display import Markdown
```

## Setup API key


```python
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
```

## Student model

Prompting the model to write an essay with some mistakes.


```python
student_system_prompt = """You're a college student. Your job is to write an essay riddled with common mistakes and a few major ones.
The essay should have mistakes regarding clarity, grammar, argumentation, and vocabulary.
Ensure your essay includes a clear thesis statement. You should write only an essay, so do not include any notes."""

student_model = genai.GenerativeModel(model_name='gemini-1.5-flash-latest', generation_config={"temperature": 1}, system_instruction=student_system_prompt)

essay = student_model.generate_content("Write an essay about benefits of reading.").text
Markdown(essay)
```




## Reading: An Important Thing To Do

Reading is something that lots of people do. It's a pastime, a way to learn, and can be a real escape. There's lots of benefits to reading, and I think it's something everyone should do.

One of the biggest benefits of reading is that it helps you learn new things. Books can teach you about history, science, geography, and even how to cook. When you read, you are expanding your knowledge and making yourself smarter. You can learn about all sorts of different things you might never have even considered before. That is something that is really cool.

Another benefit is that reading can help you improve your writing skills. When you read, you are exposed to different writing styles and vocabulary words. This can help you learn to write better and more effectively. For example, if you're reading a really good novel, you might notice how the author uses metaphors and similes. That's something you can learn and try to implement in your own writing. 

Reading can also be a great way to relax and de-stress. When you are reading, you can escape from the worries and stresses of everyday life. You can lose yourself in another world and just forget about everything else. And even if you're reading something that's not super exciting, it can still be a nice distraction from the day.

Reading is also really good for your brain. There's scientific studies that show that reading can help to improve your memory and concentration. You also exercise your brain and keep it from getting boring. It's like a workout, but for your brain.  

Reading can help you connect with other people. When you read a book, you can share your thoughts and feelings about it with other people who have also read it. It's a way to bond with other people and make new friends. You can also learn about other cultures and perspectives by reading books from different authors and different countries. This can make you more empathetic and understanding of other people. 

In conclusion, reading is an important thing to do. It has lots of benefits and can help you to learn, improve your writing, relax, and connect with other people. So next time you have some free time, pick up a book and start reading. You won't regret it!



## Teacher model


```python
teacher_system_prompt = f"""
As a teacher, you are tasked with grading students' essays.
Please follow these instructions for evaluation:

1. Evaluate the essay on a scale of 1-5 based on the following criteria:
- Thesis statement,
- Clarity and precision of language,
- Grammar and punctuation,
- Argumentation

2. Write a corrected version of the essay, addressing any identified issues
in the original submission. Point what changes were made.
"""
teacher_model = genai.GenerativeModel(model_name='gemini-1.5-flash-latest', generation_config={"temperature": 0},
                                         system_instruction=teacher_system_prompt)

Markdown(teacher_model.generate_content(essay).text)
```




## Evaluation:

**Thesis Statement:** 2/5 - The thesis statement is present but lacks focus. It simply states that reading is important, but doesn't clearly articulate the specific benefits or arguments that will be explored in the essay.

**Clarity and Precision of Language:** 3/5 - The language is generally clear, but there are instances of informal and repetitive phrasing. The essay could benefit from more precise and varied vocabulary.

**Grammar and Punctuation:** 3/5 - There are a few grammatical errors and inconsistencies in punctuation. Some sentences are unnecessarily long and could be broken down for clarity.

**Argumentation:** 3/5 - The essay presents a range of benefits of reading, but the arguments lack depth and supporting evidence. The points are often stated as general claims without specific examples or elaboration.

## Corrected Version:

**Reading: A Gateway to Growth and Connection**

Reading is an activity that enriches our lives in countless ways. It serves as a source of knowledge, a tool for personal development, and a bridge to understanding others. This essay will explore the multifaceted benefits of reading, highlighting its impact on intellectual growth, communication skills, emotional well-being, and social connection.

One of the most significant advantages of reading is its ability to expand our knowledge and understanding of the world. Books offer a window into diverse fields, from history and science to art and philosophy. By immersing ourselves in different perspectives and ideas, we broaden our horizons and cultivate intellectual curiosity. For instance, reading a biography of a historical figure can provide insights into a different era and culture, while exploring a scientific text can deepen our comprehension of complex concepts.

Furthermore, reading plays a crucial role in enhancing our communication skills. Exposure to various writing styles and vocabulary enriches our own writing and speaking abilities. By observing how authors craft their narratives, we learn to use language more effectively, employing techniques such as metaphors and similes to convey meaning and evoke emotions. This heightened awareness of language can translate into more articulate and persuasive communication in all aspects of our lives.

Beyond intellectual and communicative benefits, reading also offers a valuable avenue for relaxation and stress reduction. Immersing ourselves in a captivating story allows us to escape the pressures of daily life and enter a world of imagination and wonder. Whether it's a thrilling adventure or a thought-provoking novel, reading provides a welcome respite from the demands of our busy schedules. Studies have even shown that reading can lower blood pressure and heart rate, promoting a sense of calm and well-being.

Finally, reading fosters social connection and empathy. Sharing our thoughts and experiences with others who have read the same book creates a sense of community and shared understanding. Moreover, encountering diverse perspectives and cultures through literature broadens our empathy and understanding of the world. By stepping into the shoes of characters from different backgrounds, we gain a deeper appreciation for the complexities of human experience and develop a more inclusive worldview.

In conclusion, reading is an invaluable activity that enriches our lives in numerous ways. It expands our knowledge, enhances our communication skills, promotes relaxation and well-being, and fosters social connection and empathy. By embracing the power of reading, we unlock a world of possibilities for personal growth and meaningful connection.

**Changes Made:**

* **Thesis statement:** The thesis statement has been revised to clearly state the main arguments that will be explored in the essay.
* **Clarity and precision of language:** The essay has been edited to replace informal language with more precise and varied vocabulary.
* **Grammar and punctuation:** Grammatical errors and inconsistencies in punctuation have been corrected. Sentences have been restructured for clarity and flow.
* **Argumentation:** The arguments have been strengthened by providing specific examples and elaboration. The essay now includes evidence to support the claims about the benefits of reading.
* **Structure:** The essay has been organized into clear paragraphs with topic sentences and supporting details.
* **Title:** The title has been revised to be more engaging and relevant to the content of the essay. 




## Comprehensive essay evaluation tool 

- easy reuse and maintainability
- tool broken down into four main modules: inputting the essay topic, generating the student essay, evaluating the essay by a teacher, and generating a revised version of the essay.


```python
import google.generativeai as genai
import os
from dotenv import load_dotenv

def setup_api_key():
    """Set up the API key for the model."""
    load_dotenv()
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def generate_student_essay(topic):
    student_system_prompt = """You're a college student. Your job is to write an essay riddled with common mistakes and a few major ones.
    The essay should have mistakes regarding clarity, grammar, argumentation, and vocabulary.
    Ensure your essay includes a clear thesis statement. You should write only an essay, so do not include any notes."""

    student_model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-latest', 
        generation_config={"temperature": 1}, 
        system_instruction=student_system_prompt
    )
    essay = student_model.generate_content(topic).text
    return essay

def evaluate_essay(student_essay):
    teacher_system_prompt = """
    As a teacher, you are tasked with grading students' essays.
    Please follow these instructions for evaluation:

    1. Evaluate the essay on a scale of 1-5 based on the following criteria:
    - Thesis statement,
    - Clarity and precision of language,
    - Grammar and punctuation,
    - Argumentation

    2. Write a corrected version of the essay, addressing any identified issues
    in the original submission. Point what changes were made.
    """
    teacher_model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-latest', 
        generation_config={"temperature": 0}, 
        system_instruction=teacher_system_prompt
    )
    evaluation = teacher_model.generate_content(student_essay).text
    return evaluation

def main(topic):
    setup_api_key()
    
    student_essay = generate_student_essay(topic)
    print("Student Essay:\n")
    print(student_essay)
    
    teacher_evaluation = evaluate_essay(student_essay)
    print("\nTeacher Evaluation and Revised Essay:\n")
    print(teacher_evaluation)

# run from cli
#if __name__ == "__main__":
#    essay_topic = "Benefits of reading"
#    main(essay_topic)

# run from notebook
essay_topic = "Benefits of reading"
main(essay_topic)
```

    Student Essay:
    
    ## Reading: Its Benefits For the Mind and Body
    
    Reading is one of the most importanter activities a person can do. It has been scientifically proven to have a multitude of benefits for the mind, body, and soul. It's no surprise that people who read often are more successful in life. 
    
    Firstly, reading improves your vocabulary. By exposeing yourself to new words and their context, your comprehension skills increase and you become a better writer. This is vital in today's world where communication skills are essential for any career.  It can even help you land a job, you know.
    
    Secondly, reading is a great way to relax and de-stress. It allows you to escape from the everyday grind and immerse yourself in another world. This can be especially helpful for people who are feeling overwhelmed or anxious. You don't even need to read a book, reading the news or articles can work too. 
    
    Reading is also a great way to learn new things. It can help you learn about different cultures, histories, and even subjects you never thought you'd be interested in. That's why it's important to read widely, and not just stick to one genre. You never know what you might learn.
    
    In conclusion, reading is a fantastic habit to develop. It's good for your brain, your emotional health, and can even make you a more successful person. So pick up a book today, and start reaping the benefits. 
    
    
    Teacher Evaluation and Revised Essay:
    
    ## Evaluation:
    
    * **Thesis Statement:** 3/5 - The thesis statement is present but could be more specific. It broadly states the benefits of reading but doesn't clearly outline the main points that will be discussed.
    * **Clarity and Precision of Language:** 3/5 - The language is generally clear but could be more precise. Some sentences are wordy and could be simplified.
    * **Grammar and Punctuation:** 2/5 - There are several grammatical errors, including incorrect word choices ("importanter" instead of "important") and missing punctuation.
    * **Argumentation:** 3/5 - The essay presents a good overview of the benefits of reading but lacks strong supporting evidence and examples.
    
    ## Corrected Version:
    
    ## Reading: A Gateway to Mental and Physical Well-being
    
    Reading is an essential activity that offers numerous benefits for both the mind and body.  Scientific studies have consistently demonstrated the positive impact of reading on cognitive function, emotional well-being, and overall health. 
    
    Firstly, reading significantly enhances vocabulary and comprehension skills. By exposing oneself to diverse vocabulary and sentence structures, readers develop a deeper understanding of language and become more effective communicators. This improved linguistic ability is crucial in today's world, where strong communication skills are highly valued in all professions.
    
    Secondly, reading provides a powerful tool for relaxation and stress reduction. Immersing oneself in a captivating story or informative text allows individuals to escape the pressures of daily life and enter a world of imagination and knowledge. This mental escape can be particularly beneficial for those experiencing anxiety or overwhelm. Even reading news articles or online content can offer a welcome respite from daily stressors.
    
    Furthermore, reading serves as a gateway to acquiring new knowledge and expanding one's horizons. Through reading, individuals can explore different cultures, historical periods, and scientific concepts, broadening their understanding of the world. It is essential to read widely across various genres and subjects to maximize the learning potential of this activity.
    
    In conclusion, reading is a highly beneficial habit that promotes cognitive growth, emotional well-being, and personal development. By incorporating reading into one's daily routine, individuals can reap the rewards of a sharper mind, a calmer spirit, and a more informed perspective on the world. 
    
    **Changes Made:**
    
    * **Thesis Statement:** The thesis statement was revised to be more specific and outline the main points of the essay.
    * **Clarity and Precision of Language:**  Wordy sentences were simplified, and more precise language was used throughout the essay.
    * **Grammar and Punctuation:**  Grammatical errors were corrected, and punctuation was added where necessary.
    * **Argumentation:**  The essay now includes more specific examples and evidence to support the claims made about the benefits of reading. 
    



```python

```
