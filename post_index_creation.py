# Meant to contain page rank and offset creation files that should be run after 
# build index, and before query.py

import json
import helpers as hp



# def clean_outlinks():
#     ''' Removes any links not in corpus'''
#     outlinks_dict = create_index_offset(hp.OUTLINKS_FILE)
#     all_relevant_links = set(hp.load_json(hp.DOC_ID_FILE))
#     for offset in outlinks_dict.values():
#         new_links = []
#         for link in hp.file_json_offset_seek(offset)['links']:


@hp.memory_decorator
def create_index_offset(file_path):
    offset_dict = {} 
    offset = 0
    with open(file_path,'rb') as file:
        for line in file:
            entry = json.loads(line)
            offset_dict[entry[0]] = offset
            offset+=len(line)
    return offset_dict
