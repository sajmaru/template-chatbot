"""
This script contains functions for formatting and processing text inputs, particularly for query keywords. It is designed to be used in contexts where clean and singular-form keywords are needed, such as in search queries or data processing tasks.

Functions:
- get_keywords(text): Extracts keywords from query using text-bison model with sample inputs prompts as example
- format_text(text): Cleans and formats the input text. It removes special characters, extra spaces, and converts all words to their singular form.
- singularize_text(text): Converts all words in the input text to their singular form using the `inflect` library.

Usage:
1. Import the script or the specific functions into your project.
2. Use `format_text(text)` to clean and singularize any text input.
3. Alternatively, use `singularize_text(text)` if you only need to singularize the words without cleaning the text.

Dependencies:
- inflect: This library is used for converting words to their singular forms.
- re: The 're' module from Python's standard library is used for regular expression operations.

Example:
    formatted_text = format_text("Cats and dogs in the gardens!")
    # Output: 'Cat and dog in the garden'
"""

import inflect
import vertexai
from vertexai.language_models import TextGenerationModel

import re
from .prompt_helper import *

textgen_model = TextGenerationModel.from_pretrained("text-bison")


'''Query Keywords formating'''
def get_keywords(query):
    prompt = f"""
    {keywors_prompt_examples}
    input:
    {query}
    get keywords from the above sentence and return in a continues string
    
    output:
    """
    
    # retrieve response
    key_words = textgen_model.predict(prompt).text
    key_words_formatted = format_text(key_words)
    return key_words_formatted

def format_text(text):
    # Remove special characters, keeping only alphanumeric and certain punctuation
    text = re.sub('[^a-zA-Z0-9.?]', ' ', text)
    
    # Replace double spaces with single spaces and strip leading/trailing spaces
    text = text.replace('  ', ' ').strip()
    
    # Convert text to singular form
    text = singularize_text(text)
    return text

def singularize_text(text):
    p = inflect.engine()
    words = text.split()
    singular_words = []
    
    # Iterate over each word and singularize it
    for word in words:
        singular_word = p.singular_noun(word)
        
        # Append the singular form of the word if it exists, else append the original word
        if singular_word:
            singular_words.append(singular_word)
        else:
            singular_words.append(word)
    
    # Join the singular words back into a single string
    singular_text = ' '.join(singular_words)
    return singular_text
