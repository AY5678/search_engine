#helpers.py

#This file contains various helper functions that are used throughout the program

import json
from bs4 import BeautifulSoup

def append_to_jsonl(file_path, content):
    """
    Takes in the file path as the jsonl location and then appends
    the given content to the end of the jsonl
    """

    with open(file_path, 'a') as file:
        file.write(json.dumps(content) + '\n')

def load_json(file_path):
    """
    Given the json file path, returns the loaded json
    """

    with open(file_path) as file:
        data = json.load(file)

        return data

def get_text_content(raw_HTML, encoding):
    """
    Given a raw_HTML, returns the content using the given encoding
    """

    soup = BeautifulSoup(raw_HTML, "html.parser", from_encoding = encoding)

    #Remove the script and style elements
    for element in soup(["script", "style"]):
        element.decompose()

    #Get the text separated by words
    content = soup.get_text(separator = " ")

    #Return the content in readable format
    return " ".join(content.split())
