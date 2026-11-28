#content_generator.py

import os
from helpers import load_json, tokenize, write_file,stem
from bs4 import BeautifulSoup
import simhash as sh
from urllib.parse import urlparse, urljoin, urldefrag

NUM_HASH_BITS = 64             # hashes for simhash are 64 bits

STOP_WORDS = set("""a about above after again against all am an and any are aren't as at be because been before being below 
between both but by can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from further 
had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers herself him himself his how how's i i'd i'll 
i'm i've if in into is isn't it it's its itself let's me more most mustn't my myself no nor not of off on once only or other 
ought our ours ourselves out over own same shan't she she'd she'll she's should shouldn't so some such than that that's the 
their theirs them themselves then there there's these they they'd they'll they're they've this those through to too under until 
up very was wasn't we we'd we'll we're we've were weren't what what's when when's where where's which while who who's whom why 
why's with won't would wouldn't you you'd you'll you're you've your yours yourself yourselves""".split())

class ContentGenerator:
    """
    This is a class for providing documents from the DEV folder one at a time
    """

    def __init__(self):
        """
        Initalize starting attributes
        """

        self.document_list = []
        self.page_hashes = []

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
                    base_url = raw_json["url"]
                    base_url = urldefrag(base_url.strip())[0]
                              
                    #Get the tokenized and stemmed content

                    content,forward_links = get_contents(base_url,raw_HTML)
                    content = tokenize(content)

                    # near-word similarity.
                    is_duplicate = False
                    content_words  = [w for w in content if w not in STOP_WORDS and len(w) > 1]
                    page_hash = sh.get_simhash(content_words)

                    if sh.is_simhash_match(page_hash,self.page_hashes):
                        is_duplicate =True
                    self.page_hashes.append(page_hash)


                    content = stem(content)
                    #Return both the document id and text content
                    if is_duplicate:
                        yield None, None,None
                    else:
                        self.document_list.append(base_url)         
                        yield document_id, content, forward_links
                        document_id += 1

def get_contents(base_url,raw_HTML):
    """
    Given a raw_HTML, returns the string content, next_links
    """
    soup = BeautifulSoup(raw_HTML, "html.parser")

    next_links = _get_all_links(base_url,soup)
   
    #Remove the script and style elements
    for element in soup(["script", "style"]):
        element.decompose()

    #Get the text separated by words
    content = soup.get_text(separator = " ")

    #Return the content in readable format
    return " ".join(content.split()),next_links

def _get_all_links(base_url,soup)->list:
    ''' Takes in url and soup object, returns all links in page'''
    next_links = []
    for anchor in soup.find_all('a', href=True):
        try:
            link = urldefrag(urljoin(base_url, anchor['href'].strip()))[0]
            if urlparse(link).scheme not in ['http','https']:
                continue
        except ValueError:      # malformed href (e.g. bad IPv6 bracket host)
            continue
        next_links.append(link)
    return next_links

