import utils_crawl
import utils_wikipedia


target_qs = ['Q50729731']
# en is complete
#languages = ['nl', 'it', 'es', 'de', 'fr']
languages = ["nl"]

# number of aicles you try to crawl (set to 20 for testing)
cutoff = -1 # set to -1 to get all references

for target_q in target_qs:
    for lang in languages:
        utils_crawl.crawl_source_texts(target_q, lang, cutoff)
