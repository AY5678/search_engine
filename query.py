import helpers as hp
import json


# gets all similar documents by searching for token and returning all relevant document_ids. 
def _get_document_frequencies(tokens):
    """
    Takes a list of tokens, and finds all documents relating to it.
    Returns a list of sets, each set containing document_ids relating to a token.
    """
    #id_frequency_list = []
    id_list = []
    tokens_set = set(tokens)
    with open("inverted_index.jsonl") as file:
            for line in file:
                entry = json.loads(line)
                if entry['word'] in tokens_set:
                    #id_with_freq = []
                    doc_id = set()
                    for posting in entry["frequencies"]:
                        doc_id.add(posting['document_id'])
                        #id_frequency_list.extend((posting['document_id'],posting['frequency']))
                    id_list.append(doc_id)
                    tokens_set.remove(entry['word'])
    return id_list if not tokens_set else []

def _similar_document_ids(tokens):
    """
    From a set of tokens, it calls documents_list to get a list of sets.
    Returns a list of all document_ids which have all tokens.
    """

    documents_list = _get_document_frequencies(tokens)
    if not documents_list:
        return []
    
    doc_ids = set()
    for doc_set in documents_list:
        doc_ids.update(doc_set)
    res = []

    # AND SEARCH
    for doc_id in doc_ids:
        and_search = True
        for doc_set in documents_list:
            if doc_id not in doc_set:
                and_search = False
                break
        if and_search:
            res.append(doc_id)
    return res


def get_urls(tokens):
    urls = []
    for doc_id in _similar_document_ids(tokens):
        urls.append(DOCUMENT_IDS[doc_id])
    return urls
def run():
    while True:
        query = input("Please enter your query: ")
        tokens = hp.stem(hp.tokenize(query))
        print("Related URL's")
        i = 0
        urls = get_urls(tokens)
        if not urls:
            print("No urls found")
            continue
        for url in urls:
            if i == 5:
                break
            print(url)
            i+=1
        print("Thank you!")

if __name__ == '__main__':
    DOCUMENT_IDS = hp.load_json("document_id.json")
    run()