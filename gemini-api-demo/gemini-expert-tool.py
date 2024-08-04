import google.generativeai as genai
import os
from dotenv import load_dotenv

def setup_api_key():
    """Set up the API key for the model."""
    load_dotenv()
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def create_expert_model(system_instruction: str) -> genai.GenerativeModel:
    """Create and return a Generative AI model configured with the provided system instruction."""
    return genai.GenerativeModel(
        model_name='gemini-1.5-flash-latest',
        generation_config={"temperature": 0},
        system_instruction=system_instruction
    )

def get_expert_answer(model: genai.GenerativeModel, user_input: str) -> str:
    """
    Uses the Generative AI model to generate an answer based on the user input.
    
    Args:
        model (genai.GenerativeModel): The Generative AI model configured with the system instruction.
        user_input (str): The input from the user that the expert model will respond to.
    
    Returns:
        str: The expert's answer to the user input, in plain text format.
    """
    response = model.generate_content(user_input).text
    return response

def main():
    setup_api_key()
    
    # Define the system instruction for the expert model
    system_instruction = """
    You are an expert in a specific field. Your task is to provide precise, detailed, and well-informed answers based on the user input.
    """
    
    # Create the expert model with the system instruction
    model = create_expert_model(system_instruction)
    
    # Accept user input
    user_input = input("Enter your query for the expert: ")
    
    # Get the expert's answer
    expert_answer = get_expert_answer(model, user_input)
    
    # Print the expert's answer
    print("Expert's Answer:")
    print(expert_answer)

# run from command line
if __name__ == "__main__":
    main()

