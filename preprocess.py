from langdetect import detect
import json
import os
from collections import defaultdict


def load_texts(target_dir):
    
    text_lang_data = []
    text_path = f'corpus/{target_dir}/texts/'
    wiki_path =  f'corpus/{target_dir}/wikipedia-wikidata/'
    lang_text_paths = []
    
    for path in os.listdir(text_path):
        lang_text_paths.append(text_path+path)
        
    for path in lang_text_paths:
        lang_original = path.split('/')[-1]
        if not lang_original.startswith('.DS_Store'):
            wiki_path_lang = wiki_path+lang_original
            wiki_file = os.listdir(wiki_path_lang)
            if wiki_file:
                wiki_file = wiki_file[0]
                if wiki_file.endswith('.json'):
                    wiki_file_path = wiki_path_lang+'/'+ wiki_file
                    with open(wiki_file_path) as infile:
                        d_wiki = json.load(infile)
                    wiki_url = d_wiki['wikipedia_url']
                    q = d_wiki['wikidata_q']
                    title = d_wiki['wikipedia_title']
                    for f in os.listdir(path):
                        text_path = path+'/'+f
                        if text_path.endswith('.json'):
                            with open(text_path) as infile:
                                d = json.load(infile)
                            text = d['text'].strip()
                            if len(text) > 100 and text != title and not text.isnumeric() and ' ' in text:
                                #print(target_dir, lang_original, len(text), text_path)
                                lang_detected = detect(text)
                                #print(text_path, lang_original, lang_detected)
                                lang_d = dict()
                                lang_d['path'] = text_path
                                lang_d['lang-original'] = lang_original
                                lang_d['lang-detected'] = lang_detected
                                lang_d['wikipedia_url'] = wiki_url
                                lang_d['wikidata_q'] = q
                                lang_d['path_wikipedia']= wiki_file_path
                                lang_d['wikipedia_title'] = title

                                text_lang_data.append(lang_d)
    return text_lang_data


def sort_texts(text_lang_data, target_dir):
    
    if len(text_lang_data) > 0:
        wiki_q = text_lang_data[0]['wikidata_q']

        wiki_json_dict = dict()
        wiki_json_dict['wikidata_q'] = wiki_q
        wiki_json_dict['documents'] = defaultdict(list)
        #wiki_json_dict['wikipedia_title'] = text_lang_data[0]['wikipedia_title']
        #name = text_lang_data[0]['wikipedia_title'].strip().replace(' ', '_')
        for d in text_lang_data:
            lang_detected = d['lang-detected']
            original_path = d['path']
            original_path_base = os.path.basename(original_path)
            new_path_dir = f'corpus_clean/{target_dir}/texts/{lang_detected}'
            new_path_text = f'{new_path_dir}/{original_path_base}'
            d['path'] = new_path_text
            wiki_json_dict['documents'][lang_detected].append(d)
            os.makedirs(new_path_dir, exist_ok=True)
            with open(original_path) as infile:
                d_text = json.load(infile)
            with open(new_path_text, 'w') as outfile:
                json.dump(d_text, outfile)    
        path_wiki = f'corpus_clean/{target_dir}/wikidata.json'
        with open(path_wiki, 'w') as outfile:
            json.dump(wiki_json_dict, outfile)
        
        
def main():
    
    for subcor in os.listdir('corpus/'):
        if not subcor.startswith('.DS_Store'):
            text_lang_data = load_texts(subcor)
            sort_texts(text_lang_data, subcor)
        
if __name__ == '__main__':
    main()