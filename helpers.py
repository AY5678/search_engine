#helpers.py

#This file contains various helper functions that are used throughout the program

import json
import re
import glob
import heapq
import os
import time
from itertools import groupby
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from functools import wraps

#Create a stemmer for stemming
stemmer = PorterStemmer()

def load_json(file_path):
    """
    Given the json file path, returns the loaded json
    """

    with open(file_path, encoding = "utf-8") as file:
        data = json.load(file)

        return data

def get_text_content(raw_HTML):
    """
    Given a raw_HTML, returns the string content
    """

    soup = BeautifulSoup(raw_HTML, "html.parser")

    #Remove the script and style elements
    for element in soup(["script", "style"]):
        element.decompose()

    #Get the text separated by words
    content = soup.get_text(separator = " ")

    #Return the content in readable format
    return " ".join(content.split())

def tokenize(text):
    """
    Given some text, tokenizes it and returns it
    """

    #Put all text in lowercase format while preserving apostrophes
    text = text.lower().replace("’", "'")

    #Return the tokenized version only using alphanumeric characters
    return re.findall(r"[^\W_]+(?:'[^\W_]+)?", text)

def stem(words):
    """
    Given a list of words, returns the stemmed version of each
    word using the current stemmer
    """

    return [stemmer.stem(word) for word in words]

def _read_single_line(file_path):
    """
    Generates the next line of entry and frequencies pairing for the given file path
    """

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            entry = json.loads(line)
            yield entry["word"], entry["frequencies"]


def merge_batches(directory_path):

    """
    Searches the given directory path to merge all batches matching a specific format
    """

    #Get all the batch_files
    batches = glob.glob(os.path.join(directory_path, "batch*_index.jsonl"))

    #Merge all sorted batch files by word
    merged = heapq.merge(*(_read_single_line(path) for path in batches), 
    key=lambda entry: entry[0])

    with open("inverted_index.jsonl", "w", encoding="utf-8") as output:

        #Group entries that have the same word
        for word, entries in groupby(merged, key=lambda entry: entry[0]):

            frequencies = []

            #Combine the document-frequency lists
            for _, document_frequencies in entries:
                frequencies.extend(document_frequencies)

            #Get the combined entry
            entry = {"word": word, "frequencies": frequencies}

            #Write the combined entry
            output.write(json.dumps(entry) + "\n")

def time_decorator(func):
    """
    Serves as a wrapper function that when will record the time elapsed in milliseconds
    from running the given function

    As of milestone one, this function is unused and will be helpful later
    on for measuring the time of search queries
    """

    @wraps(func)
    def time_wrapper(*args, **kwargs):
        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        end_time = time.perf_counter()

        #Get the elapsed time in milliseconds
        elapsed_time = (end_time - start_time) * 1000

        print(f"Elapsed Time: {elapsed_time:.2f} milliseconds")

        return result
    
    return time_wrapper