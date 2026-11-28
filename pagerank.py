import helpers as hp
import json

links = {} # {link: [outlinks]}
inverted_links = {} #{"link":["list of links that point to it"]}
page_ranks = {} #{"link":"pagerank"}

doc_links = hp.load_json(hp.DOC_ID_FILE)

def get_pagerank(page, d=0.85):
    total = 0.0
    for source in inverted_links.get(page, []):
        total += page_ranks[source] / len(links[source])
    return (1 - d) + d * total

def run_pagerank(d=0.85, tolerance=0.001, max_iter=100):
    for page in links:
        page_ranks[page] = 1.0
    for _ in range(max_iter):
        new_ranks = {page: get_pagerank(page, d) for page in links}
        change = sum(abs(new_ranks[p] - page_ranks[p]) for p in links)
        page_ranks.update(new_ranks)          # actually move to the next iteration
        if change/len(links) < tolerance:
            break
    hp.write_file(json.dumps(page_ranks),hp.PAGE_RANKS_FILE)
def _load_outlinks():
    with open(hp.OUTLINKS_MODIFIED_FILE, 'r') as f:
        for line in f:
            entry = json.loads(line)
            base_link = doc_links[entry['doc_id']]
            links[base_link] = entry['links']

def _create_inverted_links():
    for base_link, outlinks in links.items():
        for outlink in outlinks:
            inverted_links.setdefault(outlink,[])\
                .append(base_link)

def run():
    _load_outlinks()
    _create_inverted_links()
    run_pagerank()
if __name__ == '__main__':
    run()
    