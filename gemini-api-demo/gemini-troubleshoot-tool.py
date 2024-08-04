import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Configure the error handling model
error_handling_system_prompt = """
Your task is to explain exactly why this error occurred and how to fix it.
"""
error_handling_model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest', 
    generation_config={"temperature": 0},
    system_instruction=error_handling_system_prompt
)

def troubleshoot_error(error_message: str) -> str:
    """
    Uses the Generative AI model to generate an explanation for the given error message.
    
    Args:
        error_message (str): The error message to troubleshoot.
    
    Returns:
        str: The content explaining the error and how to fix it, in plain text format.
    """
    error_prompt = f"""
    You've encountered the following error message:
    Error Message: {error_message}"""
    
    response = error_handling_model.generate_content(error_prompt).text
    return response

def main():
    error_message = """
       1 my_list = [1,2,3]
    ----> 2 print(my_list[3])

    IndexError: list index out of range
    """
    
    # Call the troubleshooting function and print the result
    result = troubleshoot_error(error_message)
    print(result)

# Run the main function
if __name__ == "__main__":
    main()
