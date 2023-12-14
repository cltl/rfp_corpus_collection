import utils_crawl
import utils_wikipedia


target_q = 'Q50729731'
languages = ['nl']

# number of articles you try to crawl (set to 20 for testing)
cutoff = 20

for lang in languages:
    utils_crawl.crawl_source_texts(target_q, lang, cutoff)
