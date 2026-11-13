import helpers as hp
import json
from collections import namedtuple
import math
import heapq as hq
from helpers import *

Posting = namedtuple("Posting", ['document_id','tf_score','frequency'])

# gets all similar documents by searching for token and returning all relevant document_ids. 
def _get_document_frequencies(tokens):
    """
    Takes a list of tokens, and finds all documents relating to it.
    Returns a list of sets, each set containing document_ids relating to a token.
    """

    tokens_set = {tkn:[] for tkn in tokens}
    with open("inverted_index.jsonl") as file:
        # is there any faster way to traverse this? maybe sort the words...
        for line in file:
            entry = json.loads(line)
            if entry['word'] in tokens_set:
                for posting in entry["documents"]:
                    tokens_set[entry['word']].append(Posting(posting['document_id'],posting['tf_score'],posting['frequency']))

    return tokens_set

def _similar_document_ids(tokens):
    """
    From a set of tokens, it calls documents_list to get a list of sets.
    Returns a list of all document_ids which have all tokens.
    """

    tokens_set = _get_document_frequencies(tokens)
    if not tokens_set:
        return []
    
    documents_score = {}
    for _, documents in tokens_set.items():
        if len(documents) > 0:
            df = NUMBER_OF_DOCUMENTS / len(documents)
            idf = math.log(df)
        else:
            idf = 0
        for posting in documents:
            tf_score = posting.frequency if posting.frequency > 0 else 0
            document_id = posting.document_id
            if document_id not in documents_score:
                documents_score[document_id] = 0 
            weight = (1 + math.log(tf_score)) * idf
            documents_score[document_id] +=weight

    # Number of results we want to show
    k = 5
    return hq.nlargest(k, documents_score, key=documents_score.get)

@time_decorator
def get_urls(tokens):
    """
    Gets the relevant document_ids' urls.
    """

    urls = []
    for doc_id in _similar_document_ids(tokens):
        urls.append(DOCUMENT_IDS[doc_id])
    return urls

def run():
    """
    Gets a query from the user and returns at most 
    the top 5 URLs relating to the query.
    """
    while True:

        # Get user query
        query = input("Please enter your query: ")
        tokens = hp.stem(hp.tokenize(query))

        # Get URLs
        print("Related URL's")
        urls = get_urls(tokens)
        if not urls:
            print("No urls found")
            continue
        
        # Print at most 5 of the top URLs
        for url in urls:
            print(url)

        print("Thank you!")

if __name__ == '__main__':
    DOCUMENT_IDS = hp.load_json("document_id.json")
    NUMBER_OF_DOCUMENTS = 0
    with open('stats.json', 'r') as f:
        NUMBER_OF_DOCUMENTS = int(f.read().strip().split()[-1])
    run()