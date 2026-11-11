#main.py

import tempfile
import os
from content_generator import ContentGenerator
from inverted_indexer import InvertedIndexer
from itertools import islice
from helpers import *

#Sets the maximum number of documents parsed through before the current index is uploaded
BATCH_SIZE = 500

@time_decorator
def create_index_json():
    """
    Main function for running the terminal interaction and interface
    """

    #Don't mind the name, I just named it contenter since it grabs content
    contenter = ContentGenerator()

    #Create the generator
    generator = contenter.generate_next_content("DEV")

    #Create the indexer
    indexer = InvertedIndexer()

    #Count the current batch number
    batch_number = 1

    #Use a temporary directory for storing the batch indices
    with tempfile.TemporaryDirectory() as batches:

        while True:

            #Get a batch of the specified size
            batch = list(islice(generator, BATCH_SIZE))

            #If there are no more documents, break
            if not batch:
                break

            #Index each each pair of document_ids and words
            for document_id, words in batch:
                indexer.index(document_id, words)

            #Get a file path to the temporary directory
            file_path = os.path.join(batches, f"batch{batch_number}_index.jsonl")

            #Save the index
            indexer.upload_index(file_path)

            #Optionally print out batch number for testing
            print(f"Finished batch {batch_number}")

            #Increment the batch number
            batch_number += 1

        #Combine the indexes
        merge_batches(batches)


#Safety check
if __name__ == "__main__":
    create_index_json()