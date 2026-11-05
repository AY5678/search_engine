#content_provider.py

class content_provider:
    """
    This is a class for providing documents from the DEV folder one at a time
    """

    def __init__(self):
        """
        Initalize starting attributes
        """

        #Start with a document id of 1 that will increase for each document looked at
        document_id = 1

    def generate_next_content(self):
        """
        Returns a tuple with the first object representing the document_id
        and the second representing the parsed HTML content of the document
        """

        pass