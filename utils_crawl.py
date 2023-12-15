import utils_wikipedia

# strore output
import json
import os

# access wikipedia:
# https://pypi.org/project/wikipedia/
# Wrapper for https://www.mediawiki.org/wiki/API
import wikipedia
# crawl and parse news
from newsplease import NewsPlease

# for error exceptions from NewsPlease
import newspaper
# for error exception from waybackpy
from waybackpy import cdx_utils, cdx_api
from waybackpy import WaybackMachineCDXServerAPI

# Create wayback links
from requests import adapters
import waybackpy

def crawl_source_texts(target_q, lang, cutoff = 20):

# get English Event name
    title_en = utils_wikipedia.get_wikipedia_title(target_q, 'en')
    name_en = title_en.replace(' ', '_')

    os.makedirs("corpus", exist_ok=True)
    text_dir = f"corpus/{name_en}/texts/"
    wikidata_dir = f"corpus/{name_en}/wikipedia-wikidata/"
    os.makedirs(text_dir, exist_ok=True)
    os.makedirs(wikidata_dir, exist_ok=True)
    text_dir_lang = f"corpus/{name_en}/texts/{lang}/"
    wikidata_dir_lang = f"corpus/{name_en}/wikipedia-wikidata/{lang}/"
    os.makedirs(text_dir_lang, exist_ok=True)
    os.makedirs(wikidata_dir_lang, exist_ok=True)

    print("looking for page", name_en, 'in', lang)
    # get actual page in target language
    target_title = utils_wikipedia.get_wikipedia_title(target_q, lang)
    print("Found target title", target_title)
    target_page = wikipedia.page(target_title, auto_suggest=False)
    # target_candidates = wikipedia.search(target_title, results = 10, suggestion=True)
    # print(target_candidates)
    # for cand, sugg in target_candidates:
    #     #cand_title = cand.title()
    #     print(type(cand), cand)
    #     print(type(sugg), sugg)
    #     cand_title = cand
    #     if target_title == cand_title:
    #         target_page = cand
    #         print('match!', target_page.title(), type(target_page))
    #         break
    print("Found target page")
    print(target_page)
    wikipedia_url = target_page.url
    target_references = target_page.references
    # os.makedirs('texts', exist_ok = True)
    # os.makedirs('wikipedia-wikidata', exist_ok = True)
    structured_dict = dict()
    structured_dict['wikipedia_title'] = target_title
    structured_dict['wikipedia_url'] = wikipedia_url
    structured_dict['wikidata_q'] = target_q
    structured_dict['texts'] = dict()
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:40.0) Gecko/20100101 Firefox/40.0"
    if cutoff != -1:
        target_references_sliced = target_references[:cutoff]
    else:
        target_references_sliced = target_references

    for a_id, url in enumerate(target_references_sliced):
        oldest_url = None
        try:
            cdx_api_instance = WaybackMachineCDXServerAPI(url, user_agent)
            oldest_url = cdx_api_instance.oldest().archive_url
        except cdx_utils.BlockedSiteError:
            print("Blocked Site Error")
        except cdx_api.NoCDXRecordFound:
            print("NoCDXRecordFound")
        except cdx_api.WaybackError:
            print("WaybackError")
        except adapters.ConnectionError:
            print("ConnectionError")
        a_structured_dict = dict()
        a_structured_dict['original_url'] = url
        a_structured_dict['wayback_url'] = oldest_url
        structured_dict['texts'][f'{target_q}-{a_id}'] = a_structured_dict
        if not oldest_url is None:
            try:
                article_dict = dict()
                article = NewsPlease.from_url(oldest_url, timeout = 4)
                #article.download()
                #articles.append(article)
                if not article.title is None:
                    article_dict['title'] = article.title
                else:
                    article_dict['title'] = ''
                if not article.maintext is None:
                    article_dict['text'] = article_dict['title']+'\n'+article.maintext
                else:
                    article_dict['text'] = article_dict['title']+'\n'+''
                # print(url)
                # print(oldest_url)
                article_dict['original_url'] = url
                article_dict['wayback_url'] = oldest_url
                article_dict['a_id'] = f'{target_q}-{a_id}'

                with open(f"corpus/{name_en}/texts/{lang}/{target_q}-{a_id}.json", 'w') as outfile:
                    json.dump(article_dict, outfile)
            except newspaper.ArticleException:
                print('article exception')
        else:
            continue
    with open(f'corpus/{name_en}/wikipedia-wikidata/{lang}/{target_q}.json', 'w') as outfile:
        json.dump(structured_dict, outfile)
