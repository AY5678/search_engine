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

        self.document_list = []

    def generate_next_content(self, folder_name):
        """
        Generates a tuple with the first object representing the document_id
        and the second representing the parsed HTML content of the document after
        it has been tokenized and stemmed
        """
        document_id = 0
        #Process each folder in DEV and each file in those folders
        for folder in os.scandir(folder_name):
                if folder.is_dir():
                    for file in os.scandir(folder.path):
                        #Get the raw json
                        raw_json = load_json(file)

                        #Get the raw HTML
                        raw_HTML = raw_json["content"]

                        #Increment the document_id
                        document_id += 1
                        self.document_list.append(raw_json["url"])
                        #Get the tokenized and stemmed content
                        content = get_text_content(raw_HTML)
                        content = tokenize(content)
                        content = stem(content)

                        #Return both the document id and text content
                        yield document_id, content