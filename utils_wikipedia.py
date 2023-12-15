import requests
from bs4 import BeautifulSoup
import wikipedia

def get_wikidata_link(wikipedia_title):

    #target_page = wikipedia.page(wikipedia_title)
    target_candidates = wikipedia.search(wikipedia_title, results = 5)
    for cand in target_candidates:
        cand_title = cand.title
        if wikipedia_title == cand_title:
            target_page = cand
            break


    target_url = target_page.url
    r=requests.get(target_url)
    soup = BeautifulSoup(r.text)
    #print(soup)
    wd_links = soup.findAll("li")
    #"Wikidata item" in soup.body
    for wd_link in wd_links:
        wd_url = ''
        if 'Wikidata item' in wd_link.text:
            a_element = wd_link.find("a")
            wd_url = a_element.get("href")
            break
        elif 'Wikidata-item' in wd_link.text:
            a_element = wd_link.find("a")
            wd_url = a_element.get("href")
            break
    return wd_url


def get_wikipedia_title(target_q, lang):
    languages = {lang}
    wdt_ids = [target_q]
    ids_filter='|'.join(wdt_ids)
    languages_filter='|'.join(list(map(lambda x: x + 'wiki', languages)))
    #print(languages_filter)
    params={
            'action': 'wbgetentities',
            'props': 'sitelinks',
            'ids': ids_filter,
            'sitefilter': languages_filter,
            'format': 'json'
            }

    url='https://www.wikidata.org/w/api.php?'
    r=requests.get(url, params=params)
    j=r.json()
    title = j['entities'][target_q]['sitelinks'][f'{lang}wiki']['title']
    return title
