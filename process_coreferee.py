import coreferee
import spacy
import  os
import json
from collections import defaultdict

def map_coref_to_tokens(text_dict):

    token_ids = text_dict['id_token']
    coref_chains = text_dict['coref_id']
    coref_chains_read = []

    for chain in coref_chains:
        chain_dict = defaultdict(list)
        for expr in chain:
            expr_str = ''
            for tok_id in expr:
                tok = token_ids[tok_id]
                expr_str += tok
            chain_dict[expr_str].append(expr)
        coref_chains_read.append(chain_dict)

    text_dict['coref'] = coref_chains_read

def create_doc_json(doc, text_dict):
    # doc_dict = dict()
    # doc_dict['text'] = doc.text
    text_dict['coref_id'] = []

    for n, ch in enumerate(doc._.coref_chains.chains):
        ch_l = []
        for i in ch:
            expr = [int(tok_id) for tok_id in i]
            #print(type(expr[0]))
            ch_l.append(expr)

        text_dict['coref_id'].append(ch_l)


    text_dict['id_token'] = []
    text_dict['id_token_offset'] = []
    for sent in doc.sents:
        for tok in sent:
            text_dict['id_token'].append(tok.text)
            offs_start = tok.idx
            offs_end = tok.idx + len(tok.text)
            offs_dict = dict()
            offs_dict['start'] = offs_start
            offs_dict['end'] = offs_end
            text_dict['id_token_offset'].append(offs_dict)



def main():
    event_name = "Eurovision_Song_Contest_2021"

    event_names = []
    for subdir in os.listdir('corpus_clean/'):
        if not subdir.startswith('.DS_Store'):
            event_names.append(subdir)
    lang = "en"
    if lang  == 'en':
        nlp = spacy.load('en_core_web_trf')
    elif lang == 'fr':
        nlp = spacy.load('en_core_web_trf')
    elif lang == 'de':
        nlp = spacy.load('de_core_news_lg')
    elif lang == 'pl':
        nlp = spacy.load('pl_core_news_lg')

    nlp.add_pipe('coreferee')

    for event_name in event_names:

        json_dir = f'corpus_clean/{event_name}/texts/{lang}'
        #os.makedirs(json_dir, exist_ok=True)
        for f in os.listdir(json_dir):
            if f.endswith(".json"):
                path = f"{json_dir}/{f}"
                with open(path) as infile:
                    text_dict = json.load(infile)
                doc = nlp(text_dict['text'])
                create_doc_json(doc, text_dict)
                map_coref_to_tokens(text_dict)
                if 'coref_tok' in text_dict:
                    text_dict.pop('coref_tok')
                if 'coref_id' in text_dict:
                    text_dict.pop('coref_id')
                with open(path, 'w') as outfile:
                    json.dump(text_dict, outfile, indent=4)

if __name__ == "__main__":
    main()
