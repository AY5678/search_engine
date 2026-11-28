#inverted_indexer.py

import json
from collections import Counter

class InvertedIndexer:
    """
    Class representing the indexer that interacts with the
    inverted index in inverted_index.csv

    Utilizes inverted indexing
    """

    def __init__(self):
        """
        Initalize an empty inverted index
        """

        self.inverted_index = {}
        self.links = {}


    def index(self, document_id, words, forward_links):
        """
        Given a document id, the processed words it contains, and all the links it points to
        it adds it to the inverted index
        """

        #Total the count of each word
        word_counts = Counter(words)
        n = word_counts.total()

        #Process each frequency counted for each word
        for word, freq in word_counts.items():
            
            # calculates tf_score for each document. 
            tf_score = freq/n

            #If the word isn't in the index, then add a blank row
            self.inverted_index.setdefault(word, []).append(
                {"document_id": document_id, "tf_score": tf_score, "frequency" : freq})
            
            self.links[document_id] = forward_links
    def upload_index(self, inverted_index_path,links_path):
        """
        Uploads the current index to the given file path
        """

        with open(inverted_index_path, "w", encoding = "utf-8") as file:

            #Create an entry for each word and document frequency list pairing
            for word in sorted(self.inverted_index):
                documents_info = self.inverted_index[word]
                document_frequencies = {"word" : word, "documents" : documents_info}

                #Add the new entry to its corresponding json entry
                file.write(json.dumps(document_frequencies) + '\n')

            self.inverted_index = {}

        with open(links_path, "w", encoding='utf-8') as file:
            for doc_id in sorted(self.links):

                links_info = self.links[doc_id]
                links_freq = {"doc_id":doc_id, "outlinks":links_info}
                file.write(json.dumps(links_freq) + '\n')

            self.links = {}