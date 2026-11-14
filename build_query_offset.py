import json
import tracemalloc
import time
tracemalloc.start()
start_time = time.perf_counter()

word_offset_dict = {} 
offset = 0
with open("inverted_index.jsonl",'rb') as file:
    for line in file:
        entry = json.loads(line)
        word_offset_dict[entry['word']] = offset
        offset+=len(line)
current, peak = tracemalloc.get_traced_memory()
end_time = time.perf_counter()
print(f"Current: {current / 1024**2:.2f} MB | Peak: {peak / 1024**2:.2f} MB")
#Get the elapsed time in milliseconds
elapsed_time = (end_time - start_time) * 1000

print(f"Elapsed Time: {elapsed_time:.2f} milliseconds")
tracemalloc.stop()
