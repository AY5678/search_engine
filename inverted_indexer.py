#inverted_index.py

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

        #Process each frequency counted for each word
        for word, frequency in word_counts.items():

            #If the word isn't in the index, then add a blank row
            self.inverted_index.setdefault(word, []).append(
                {"document_id": document_id,"frequency": frequency})

    def upload_index(self, file_path):
        """
        Uploads the current index to the given file path
        """

        with open(file_path, "w", encoding = "utf-8") as file:
            for word, frequencies in self.inverted_index.items():
                pair = {"word" : word, "frequencies" : frequencies}

                file.write(json.dumps(entry) + '\n')