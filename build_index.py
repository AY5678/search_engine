#main.py

import tempfile
import os
from content_generator import ContentGenerator
from inverted_indexer import InvertedIndexer
from itertools import islice
from helpers import *

#Sets the maximum number of documents parsed through before the current index is uploaded
BATCH_SIZE = 500

DEV_FILE = "ANALYST"

@time_decorator
@memory_decorator
def create_index_json():
    """
    Creates the index for the pages in batches
    """

    #Don't mind the name, I just named it contenter since it grabs content
    contenter = ContentGenerator()

    #Create the generator
    generator = contenter.generate_next_content(DEV_FILE)

    #Create the indexer
    indexer = InvertedIndexer()

    #Count the current batch number
    batch_number = 1
    total_no_documents = 0
    #Use a temporary directory for storing the batch indices
    with tempfile.TemporaryDirectory() as batches:

        while True:

            #Get a batch of the specified size
            batch = list(islice(generator, BATCH_SIZE))

            #If there are no more documents, break
            if not batch:
                break

            #Index each each pair of document_ids and words
            for document_id, words, forward_links in batch:
                if document_id is None:
                    continue
                total_no_documents += 1
                indexer.index(document_id, words,forward_links)

            #Get a file path to the temporary directory
            inverted_index_path = os.path.join(batches, f"batch{batch_number}_index.jsonl")
            links_path = os.path.join(batches, f"batch{batch_number}_links.jsonl")
            #Save the index
            indexer.upload_index(inverted_index_path,links_path)

            #Optionally print out batch number for testing
            print(f"Finished batch {batch_number}")

            #Increment the batch number
            batch_number += 1

        #Combine the indexes
        merge_batches(batches)
        write_file(json.dumps([url for url in contenter.document_list]), DOC_ID_FILE)
        write_file(f"Total no of documents: {total_no_documents}", STATS_FILE)


#Safety check
if __name__ == "__main__":
    create_index_json()