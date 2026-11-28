# Meant to contain page rank and offset creation files that should be run after 
# build index, and before query.py

import json
import helpers as hp
import pagerank as pr

def clean_outlinks():
    ''' Removes any links not in corpus and save it to outlinks file'''
    # needed for pagerank
    all_relevant_links = set(hp.load_json(hp.DOC_ID_FILE))
    with open('outlinks.jsonl','r') as f:
        with open('outlinks_modified.jsonl',"w", encoding="utf-8") as out:
            tmp_path = out.name 
            for line in f:
                entry = json.loads(line)
                new_links = []
                for link in entry['links']:
                    if link  in all_relevant_links:
                        new_links.append(link)
                out.write(json.dumps({'doc_id':entry['doc_id'],'links':new_links}) + '\n')

@hp.memory_decorator
def create_index_offset(file_path):
    offset_dict = {} 
    offset = 0
    with open(file_path,'rb') as file:
        for line in file:
            entry = json.loads(line)
            key = entry[next(iter(entry))]
            offset_dict[key] = offset
            offset+=len(line)
    return offset_dict


if __name__ == '__main__':
    clean_outlinks()
    pr.run()
    
