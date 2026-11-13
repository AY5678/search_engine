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


    def index(self, document_id, words):
        """
        Given a document id and the processed words it contains, adds it to the
        inverted index
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

    def upload_index(self, file_path):
        """
        Uploads the current index to the given file path
        """

        with open(file_path, "w", encoding = "utf-8") as file:

            #Create an entry for each word and document frequency list pairing
            for word in sorted(self.inverted_index):
                documents_info = self.inverted_index[word]

                document_frequencies = {"word" : word, "documents" : documents_info}

                #Add the new entry to its corresponding json entry
                file.write(json.dumps(document_frequencies) + '\n')

            self.inverted_index = {}