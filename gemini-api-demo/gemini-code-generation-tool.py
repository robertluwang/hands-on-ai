import google.generativeai as genai
import os
from dotenv import load_dotenv

def setup_api_key():
    """Set up the API key for the model."""
    load_dotenv()
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def create_code_generation_model():
    """Create and return a code generation model."""
    code_generation_system_prompt = """
    You are a coding assistant. Your task is to generate a code snippet that accomplishes a specific goal.
    The code snippet must be concise, efficient, and well-commented for clarity.
    Consider any constraints or requirements provided for the task.

    If the task does not specify a programming language, default to Python.
    """
    return genai.GenerativeModel(
        model_name='gemini-1.5-flash-latest',
        generation_config={"temperature": 0},
        system_instruction=code_generation_system_prompt
    )

def generate_code(prompt):
    """Generate code based on the provided prompt."""
    model = create_code_generation_model()
    response = model.generate_content(prompt)
    return response.text

def main():
    setup_api_key()
    code_generation_prompt = 'write code to convert text format from DOS to Linux'
    generated_code = generate_code(code_generation_prompt)
    print(generated_code)

if __name__ == "__main__":
    main()
