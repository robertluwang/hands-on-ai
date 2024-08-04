# Gemini code generation demo

This is demo how to use prompting to perform basic code generation using the Gemini API.

Two use cases: 
- error handling
- code generation

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

## Error handling


```python
error_handling_system_prompt =f"""
Your task is to explain exactly why this error occurred and how to fix it.
"""
error_handling_model = genai.GenerativeModel(model_name='gemini-1.5-flash-latest', generation_config={"temperature": 0},system_instruction=error_handling_system_prompt)
```


```python
error_message = """
   1 my_list = [1,2,3]
----> 2 print(my_list[3])

IndexError: list index out of range
"""

error_prompt = f"""
You've encountered the following error message:
Error Message: {error_message}"""

Markdown(error_handling_model.generate_content(error_prompt).text)
```




The error message "IndexError: list index out of range" means you're trying to access an element in a list using an index that doesn't exist.

**Explanation:**

* **List Indexing:** In Python, lists are zero-indexed. This means the first element has an index of 0, the second element has an index of 1, and so on.
* **Your Code:** Your code `print(my_list[3])` is trying to access the element at index 3 in the list `my_list`.
* **The Problem:** The list `my_list` only has three elements (1, 2, and 3), with indices 0, 1, and 2. There is no element at index 3.

**How to Fix It:**

1. **Check the Index:** Make sure the index you're using is within the valid range of the list. In this case, the valid indices are 0, 1, and 2.
2. **Adjust the Index:** If you want to access the last element of the list, use `my_list[-1]`. This will access the element at index 2 (the last element).
3. **Use `len()`:** To find the length of the list, use `len(my_list)`. This will tell you the number of elements in the list, which can help you avoid out-of-range errors.

**Corrected Code:**

```python
my_list = [1, 2, 3]
print(my_list[2])  # Access the last element (index 2)
```

**Or:**

```python
my_list = [1, 2, 3]
print(my_list[-1])  # Access the last element using negative indexing
```

**Remember:** Always double-check your indices to ensure they are within the bounds of your list to avoid this error. 




Another error message 


```python
error_message = """
gemini pro api error:
'code': 400, 'message': 'Request contains an invalid argument.'
"""

error_prompt = f"""
You've encountered the following error message:
Error Message: {error_message}"""

Markdown(error_handling_model.generate_content(error_prompt).text)
```




This error message indicates that your request to the Gemini Pro API is malformed. The API server is rejecting your request because it contains an invalid argument. 

Here's a breakdown of the error and how to fix it:

**Understanding the Error:**

* **`code: 400`:** This is a standard HTTP status code indicating a "Bad Request". It means the server understood your request but couldn't process it due to an error in the request itself.
* **`message: 'Request contains an invalid argument.'`:** This specific message from Gemini Pro API tells you that the problem lies within the data you're sending in your request. 

**Common Causes of Invalid Arguments:**

* **Incorrect Parameters:** You might be using the wrong parameter names, data types, or values in your request. Double-check the Gemini Pro API documentation for the correct parameters and their expected formats.
* **Missing Parameters:**  The API might require certain parameters to be present in your request. Ensure you're including all necessary parameters.
* **Invalid Values:**  The values you're providing for parameters might be outside the acceptable range or format. For example, a price parameter might need to be a decimal number, but you're sending a string.
* **Incorrect Request Method:** You might be using the wrong HTTP method (e.g., GET instead of POST) for the API endpoint.
* **Authentication Issues:** If the API requires authentication, you might have provided incorrect credentials or your authentication token might have expired.

**How to Fix the Error:**

1. **Review the API Documentation:** Carefully examine the Gemini Pro API documentation for the specific endpoint you're using. Pay close attention to:
    * **Required parameters:** Ensure you're including all mandatory parameters.
    * **Parameter types:** Make sure you're using the correct data types (e.g., string, integer, decimal).
    * **Parameter values:** Verify that the values you're providing are within the acceptable range and format.
    * **Request method:** Confirm you're using the correct HTTP method (GET, POST, PUT, DELETE).
2. **Check Your Code:**  Inspect your code thoroughly to identify any potential errors:
    * **Parameter names:** Ensure you're using the correct parameter names as specified in the documentation.
    * **Data types:** Double-check that you're converting data to the correct types before sending it to the API.
    * **Value formatting:** Make sure your values are formatted correctly (e.g., using the right decimal separator).
3. **Test with a Simple Request:**  Start with a basic request to the API endpoint to isolate the problem. If the simple request works, gradually add complexity to your request until you identify the source of the error.
4. **Verify Authentication:** If the API requires authentication, ensure you're using the correct credentials and that your authentication token is valid.
5. **Use a Debugging Tool:**  Use a debugging tool like Postman or curl to send requests to the API and inspect the response headers and body. This can help you identify the specific error in your request.

**Example:**

Let's say you're trying to place an order using the Gemini Pro API, but you're getting the "invalid argument" error. You might have forgotten to include the `symbol` parameter in your request, or you might be providing an invalid `amount` value.

**Remember:**  The specific solution will depend on the details of your request and the Gemini Pro API endpoint you're using. 




Let's wrap the error troubleshoot reuse tool.

## Troubleshoot tool


```python
import google.generativeai as genai
import os
from dotenv import load_dotenv

def setup_api_key():
    """Set up the API key for the model."""
    load_dotenv()
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def create_error_handling_model():
    """Create and return an error handling model."""
    error_handling_system_prompt = """
    Your task is to explain exactly why this error occurred and how to fix it.
    """
    return genai.GenerativeModel(
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
    model = create_error_handling_model()
    error_prompt = f"""
    You've encountered the following error message:
    Error Message: {error_message}
    """
    
    response = model.generate_content(error_prompt).text
    return response

def main():
    setup_api_key()
    error_message = """
    1 my_list = [1,2,3]
    ----> 2 print(my_list[3])

    IndexError: list index out of range
    """
    
    # Call the troubleshooting function and print the result
    result = troubleshoot_error(error_message)
    print(result)

if __name__ == "__main__":
    main()

# run in notebook
main()

```

    The error message "IndexError: list index out of range" means you're trying to access an element in the list that doesn't exist.
    
    **Explanation:**
    
    * **List Indexing:** In Python, lists are zero-indexed. This means the first element is at index 0, the second at index 1, and so on.
    * **Your Code:** You're trying to access `my_list[3]`. However, your list `my_list` only has three elements (1, 2, and 3), which are at indices 0, 1, and 2 respectively. There is no element at index 3.
    
    **How to Fix It:**
    
    1. **Adjust the Index:**  Since your list has three elements, the valid indices are 0, 1, and 2. To access the last element, use `my_list[2]`.
    
       ```python
       my_list = [1, 2, 3]
       print(my_list[2])  # This will print 3
       ```
    
    2. **Use Negative Indexing:** Python allows negative indexing to access elements from the end of the list.  `my_list[-1]` refers to the last element, `my_list[-2]` to the second-to-last, and so on.
    
       ```python
       my_list = [1, 2, 3]
       print(my_list[-1])  # This will print 3
       ```
    
    3. **Check List Length:** Before accessing an element, you can check the length of the list using `len(my_list)`. This helps avoid errors if the list is shorter than expected.
    
       ```python
       my_list = [1, 2, 3]
       if len(my_list) > 3:
           print(my_list[3])
       else:
           print("List is too short")
       ```
    
    Remember to always be mindful of the size of your lists and use valid indices to avoid this error. 
    
    The error message "IndexError: list index out of range" means you're trying to access an element in the list that doesn't exist.
    
    **Explanation:**
    
    * **List Indexing:** In Python, lists are zero-indexed. This means the first element is at index 0, the second at index 1, and so on.
    * **Your Code:** You're trying to access `my_list[3]`. However, your list `my_list` only has three elements (1, 2, and 3), which are at indices 0, 1, and 2 respectively. There is no element at index 3.
    
    **How to Fix It:**
    
    1. **Adjust the Index:**  Since your list has three elements, the valid indices are 0, 1, and 2. To access the last element, use `my_list[2]`.
    
       ```python
       my_list = [1, 2, 3]
       print(my_list[2])  # This will print 3
       ```
    
    2. **Use Negative Indexing:** Python allows negative indexing to access elements from the end of the list.  `my_list[-1]` refers to the last element, `my_list[-2]` to the second-to-last, and so on.
    
       ```python
       my_list = [1, 2, 3]
       print(my_list[-1])  # This will print 3
       ```
    
    3. **Check List Length:** Before accessing an element, you can check the length of the list using `len(my_list)`. This helps avoid errors if the list is shorter than expected.
    
       ```python
       my_list = [1, 2, 3]
       if len(my_list) > 3:
           print(my_list[3])
       else:
           print("List is too short")
       ```
    
    Remember to always be mindful of the size of your lists and use valid indices to avoid this error. 
    


### Code generation


```python
code_generation_system_prompt = f"""
You are a coding assistant. Your task is to generate a code snippet that accomplishes a specific goal.
The code snippet must be concise, efficient, and well-commented for clarity.
Consider any constraints or requirements provided for the task.

If the task does not specify a programming language, default to Python.
"""
code_generation_model = genai.GenerativeModel(model_name='gemini-1.5-flash-latest', generation_config={"temperature": 0},system_instruction=code_generation_system_prompt)
```


```python
code_generation_prompt = 'write code to convert text format from DOS to Linux'

Markdown(code_generation_model.generate_content(code_generation_prompt).text)
```




```python
def dos2unix(input_file, output_file):
  """Converts a text file from DOS to Linux format.

  Args:
    input_file: The path to the input file in DOS format.
    output_file: The path to the output file in Linux format.
  """

  with open(input_file, 'r', encoding='latin-1') as f_in, \
       open(output_file, 'w', encoding='utf-8') as f_out:
    for line in f_in:
      # Replace DOS line endings (CRLF) with Linux line endings (LF)
      line = line.replace('\r\n', '\n')
      f_out.write(line)

# Example usage:
dos2unix('input.txt', 'output.txt')
```

**Explanation:**

1. **Function Definition:**
   - The code defines a function `dos2unix` that takes two arguments: `input_file` (path to the DOS file) and `output_file` (path to the output Linux file).

2. **File Handling:**
   - It opens the input file in read mode (`'r'`) with `latin-1` encoding, which is commonly used for DOS files.
   - It opens the output file in write mode (`'w'`) with `utf-8` encoding, which is the standard encoding for Linux.

3. **Line-by-Line Conversion:**
   - It iterates through each line in the input file.
   - For each line, it replaces the DOS line ending (`\r\n`) with the Linux line ending (`\n`) using the `replace()` method.
   - The modified line is then written to the output file.

4. **Example Usage:**
   - The code demonstrates how to call the `dos2unix` function with specific input and output file names.

**Note:**

- This code assumes that the input file is encoded in `latin-1`. If your input file uses a different encoding, you need to adjust the encoding parameter in the `open()` function accordingly.
- This code only converts the line endings. It does not handle any other potential differences between DOS and Linux text formats.




Let's wrap code generation demo to a reuse tool. 

## Code generation tool


```python
import google.generativeai as genai
import os
from dotenv import load_dotenv

def setup_genai():
    """Set up the Generative AI configuration."""
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
    setup_genai()
    code_generation_prompt = 'write code to convert text format from DOS to Linux'
    generated_code = generate_code(code_generation_prompt)
    print(generated_code)

#run from cli
#if __name__ == "__main__":
    #main()

#run in notebook
main()
```

    ```python
    import os
    
    def dos2unix(input_file, output_file=None):
      """Converts a text file from DOS to Linux format.
    
      Args:
        input_file: Path to the input file.
        output_file: Path to the output file. If None, the input file will be overwritten.
    
      Returns:
        None
      """
    
      # Read the file contents
      with open(input_file, 'r', encoding='latin-1') as f:
        content = f.read()
    
      # Replace DOS line endings (CRLF) with Linux line endings (LF)
      content = content.replace('\r\n', '\n')
    
      # Write the modified content to the output file
      if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
          f.write(content)
      else:
        with open(input_file, 'w', encoding='utf-8') as f:
          f.write(content)
    
    # Example usage:
    input_file = 'my_dos_file.txt'
    output_file = 'my_linux_file.txt'
    
    dos2unix(input_file, output_file)
    ```
    
    **Explanation:**
    
    1. **Import `os` module:** This module provides functions for interacting with the operating system, including file operations.
    2. **`dos2unix` function:**
       - Takes `input_file` and optional `output_file` as arguments.
       - Opens the input file in read mode (`'r'`) with `latin-1` encoding, which is commonly used for DOS files.
       - Reads the entire file content into the `content` variable.
       - Replaces all occurrences of `\r\n` (carriage return followed by newline) with `\n` (newline).
       - Opens the output file in write mode (`'w'`) with `utf-8` encoding, which is a common encoding for Linux files.
       - Writes the modified content to the output file. If `output_file` is not provided, the input file is overwritten.
    3. **Example usage:**
       - Sets `input_file` and `output_file` variables to the desired file paths.
       - Calls the `dos2unix` function to convert the file.
    
    **Note:**
    
    - This code assumes that the input file is in DOS format (using CRLF line endings).
    - The `latin-1` encoding is used for reading the input file, as it is a common encoding for DOS files.
    - The `utf-8` encoding is used for writing the output file, as it is a common encoding for Linux files.
    - If you encounter issues with encoding, you may need to adjust the encoding used for reading and writing the files.
    - You can use this code to convert multiple files by iterating over a list of file paths.
    


## Conclusion

In this demonstration, we explored the capabilities of the Gemini API for both error handling and code generation tasks, showcasing its potential to streamline coding processes and enhance troubleshooting efforts.

**Error Handling:**
We learned how to configure the Gemini API to handle and explain errors. By providing the system with error messages and using a model designed for error diagnosis, we can receive detailed explanations and solutions for various coding issues. The example of handling error illustrated the model's ability to provide practical advice for correcting out-of-range list accesses, emphasizing the importance of checking index bounds and using appropriate indexing techniques.

**Code Generation:**
The demonstration also covered how to generate code snippets using the Gemini API. We saw how the model can produce well-commented and efficient code based on specific prompts. For instance, generating a function to convert text file formats from DOS to Linux showed the model’s proficiency in understanding and executing coding tasks. This feature is particularly useful for automating repetitive coding tasks and generating boilerplate code efficiently.

**Reusable Tools:**
We developed reusable tools for both error troubleshooting and code generation. The `troubleshoot_error` function encapsulates the error-handling process, making it easy to troubleshoot different errors by simply providing the error message. Similarly, the `generate_code` function simplifies code generation by taking a prompt and producing the corresponding code snippet.

Overall, the Gemini API's capabilities in error handling and code generation highlight its potential to improve productivity and accuracy in coding tasks. By integrating these tools into your workflow, you can streamline error resolution and code creation processes, leading to more efficient and effective development practices.



```python

```
