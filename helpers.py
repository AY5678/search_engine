#helpers.py

#This file contains various helper functions that are used throughout the program

import json
import re
import glob
import heapq
import os
import time
from itertools import groupby
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from functools import wraps
import tracemalloc

DOC_ID_FILE = "document_id.json"
STATS_FILE = "stats.json"
INVERTED_INDEX_FILE = "inverted_index.jsonl"
OUTLINKS_FILE='outlinks.jsonl'
OUTLINKS_MODIFIED_FILE='outlinks_modified.jsonl'
PAGE_RANKS_FILE= 'page_ranks.txt'


#Create a stemmer for stemming
stemmer = PorterStemmer()

def stem(words):
    """
    Given a list of words, returns the stemmed version of each
    word using the current stemmer
    """
    return [stemmer.stem(word) for word in words]

def write_file(data, file_path):
    """ Writes data to file_path """
    
    with open(file_path,encoding = "utf-8", mode='w') as file:
        file.write(data)

def load_json(file_path):
    """
    Given the json file path, returns the loaded json
    """

    with open(file_path, encoding = "utf-8") as file:
        data = json.load(file)

        return data
def tokenize(text):
    """
    Given some text, tokenizes it and returns it
    """

    #Put all text in lowercase format while preserving apostrophes
    text = text.lower().replace("’", "'")

    #Return the tokenized version only using alphanumeric characters
    return re.findall(r"[^\W_]+(?:'[^\W_]+)?", text)


def _read_single_line(file_path):
    """
    Generates the next line of entry and frequencies pairing for the given file path
    """

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            entry = json.loads(line)
            try:
                yield entry["word"], entry["documents"]
            except:
                yield entry['doc_id'],entry['outlinks']

def merge_batches(directory_path):

    """
    Searches the given directory path to merge all batches matching a specific format
    """

    #Get all the batch_files
    index_batches = glob.glob(os.path.join(directory_path, "batch*_index.jsonl"))

    link_batches = glob.glob(os.path.join(directory_path, "batch*_links.jsonl"))
    #Merge all sorted batch files by word
    #entry[0] == word
    merged_indexes = heapq.merge(*(_read_single_line(path) for path in index_batches), 
    key=lambda entry: entry[0])

    with open("inverted_index.jsonl", "w", encoding="utf-8") as output:

        #Group entries that have the same word
        for word, entries in groupby(merged_indexes, key=lambda entry: entry[0]):

            frequencies = []

            #Combine the document-frequency lists
            for _, documents in entries:
                frequencies.extend(documents)

            #Get the combined entry
            entry = {"word": word, "documents": frequencies}

            #Write the combined entry
            output.write(json.dumps(entry) + "\n")
            
    # TODO: confirm if this sorting is required when building offsets.
    merged_links = heapq.merge(*(_read_single_line(path) for path in link_batches))

    with open("outlinks.jsonl", "w", encoding="utf-8") as output:

        #Group entries that have the same word
        for doc_id, entries in groupby(merged_links, key=lambda entry: entry[0]):
            links = []
            #Combine the document-frequency lists
            for _, outlinks in entries:
                links.extend(outlinks)

            #Get the combined entry
            entry = {"doc_id": doc_id, "links": links}

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

def memory_decorator(func):
    """
    Serves as a wrapper function that when will record the peak memory used
    from running the given function

    As of milestone one, this function is unused and will be helpful later
    on for measuring the memory usage of search queries.
    """

    @wraps(func)
    def memory_wrapper(*args, **kwargs):
        tracemalloc.start()
        try:
            res = func(*args,**kwargs)
        finally:
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            print(f"Peak: {peak / 1024**2:.2f} MB")
        return res
    return memory_wrapper


def file_json_offset_seek(file_path,offset):
    """ Reads a .jsonl file and returns a json object"""
    with open(file_path, 'rb') as f:
        pos = f.seek(offset)
        line = f.readline()
        data = json.loads(line)
    return data