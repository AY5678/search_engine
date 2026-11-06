#M1_report.py

#This file generates the diagnostics for the report

import json
import os

def get_diagnostics(file_path):
    """
    Gets the number of unique words, number of documents, and index size at the specified file path
    """

    unique_words = 0
    document_ids = set()

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            entry = json.loads(line)
            unique_words += 1

            for posting in entry["frequencies"]:
                document_ids.add(posting["document_id"])

    file_size = os.path.getsize(file_path)

    print(f"Indexed documents: {len(document_ids):,}")
    print(f"Unique words: {unique_words:,}")
    print(f"Index size: {file_size / 1024 :.2f} KB")

if __name__ == "__main__":
    get_diagnostics("inverted_index.jsonl")