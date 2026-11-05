#helpers.py

#This file contains various helper functions that are used throughout the program

import json

def append_to_jsonl(file_path, content):
    """
    Takes in the file_path as the jsonl location and then appends
    the given content to the end of the jsonl
    """

    with open(file_path, 'a') as file:
        file.write(json.dumps(content) + '\n')