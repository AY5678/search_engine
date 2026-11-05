#content_generator.py

import os
from helpers import load_json, get_text_content, tokenize, stem

class ContentGenerator:
    """
    This is a class for providing documents from the DEV folder one at a time
    """

    def __init__(self):
        """
        Initalize starting attributes
        """

        #Start with a document id of 0 that will increase for each document looked at
        #The id starts at 0 because it is incremented before each return
        self.document_id = 0

    def generate_next_content(self):
        """
        Generates a tuple with the first object representing the document_id
        and the second representing the parsed HTML content of the document after
        it has been tokenized and stemmed
        """

        #Process each folder in DEV and each file in those folders
        for folder in os.scandir("DEV"):
                for file in os.scandir(folder.path):

                    #Get the raw json
                    raw_json = load_json(file)

                    #Get the raw HTML
                    raw_HTML = raw_json["content"]

                    #Increment the document_id
                    self.document_id += 1

                    #Get the tokenized and stemmed content
                    content = get_text_content(raw_HTML)
                    content = tokenize(content)
                    content = stem(content)

                    #Return both the document id and text content
                    yield self.document_id, content