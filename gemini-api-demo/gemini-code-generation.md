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
error_handling_model = genai.GenerativeModel(model_name='gemini-1.5-flash-latest', generation_config={"temperature": 0},
                                             system_instruction=error_handling_system_prompt)
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




### Code generation


```python
code_generation_system_prompt = f"""
You are a coding assistant. Your task is to generate a code snippet that accomplishes a specific goal.
The code snippet must be concise, efficient, and well-commented for clarity.
Consider any constraints or requirements provided for the task.

If the task does not specify a programming language, default to Python.
"""
code_generation_model = genai.GenerativeModel(model_name='gemini-1.5-flash-latest', generation_config={"temperature": 0},
                                             system_instruction=code_generation_system_prompt)
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




## Conclusion

This demo highlights the capabilities of the Gemini API for two primary use cases: **error handling** and **code generation**. By using tailored prompts, the API can effectively generate explanations for errors and produce well-structured code snippets.

### Error Handling
- The demo shows how the API can provide detailed explanations for common programming errors, such as the "IndexError: list index out of range."
- This functionality is invaluable for debugging and educational purposes, offering step-by-step guidance on understanding and resolving issues.

### Code Generation
- The demo illustrates how to prompt the API to generate a Python function that converts text files from DOS to Linux format.
- The generated code includes comprehensive comments and a clear structure, ensuring ease of understanding and adaptability for various use cases.

### Overall Benefits
- The Gemini API proves to be a powerful tool for both novice and experienced programmers, enhancing their ability to debug and generate code efficiently.
- By leveraging AI-driven prompts, developers can save time and focus on more complex aspects of their projects.

This demo showcases how the Gemini API can be a valuable asset in the toolkit of any programmer, streamlining the coding process and improving overall productivity.



```python

```
