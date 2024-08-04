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
if __name__ == "__main__":
    essay_topic = "Benefits of reading"
    main(essay_topic)

