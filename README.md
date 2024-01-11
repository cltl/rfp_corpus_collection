# rfp_corpus_collection

This repositroy contains a referentially grounded corpus consisting of texts about the Eurovision Song Festival (2019, 2020, 2021) and its participants in several different languages. The corpus serves as an (un)shared dataset for the 1st Workshop in Reference, Framing, and Perspective (LREC-COLING 2024).

## Quick start

The clean and preprocessed version of the corpus can be found in `corpus_clean`. Each folder in `corpus_clean` represents a specific Eurovision Event or an entity (artist) participating in a Eurovision event (as they are represented in Wikidata and Wikipedia). We use the example of the event `Eurovision Song Contest 2021` to illustrate the structure of the subcorpora:

Eurovision_Song_Contest_2021/

       texts/
           bg/
              Q104301564-0.json
              Q104301564-1.json
              ...
           cs/
              Q104301564-0.json
              Q104301564-1.json
              ...
           de/
              Q104301564-0.json
              Q104301564-1.json
              ...
           ...
       wikipedia.json

The directory `texts` contains texts crawled via the Wikipedia pages about the event in different languages. For example, the Wikipedia page written in Bulgarian (bg) listed x many reference texts, y of which are included in the corpus. Each text is identified by the idenifier of the referent it is about (person or event) and an index (e.g. Q104301564-0). The texts are presented in json format and contain (at least) the raw text. For some texts, we provide manual or automatic annotations (FrameSemantic annotations, coreference, entity linking).

The file called `wikipdedia.json` contains an overview of the subcorpus and information about the origin of individual documents. It can be used to quickly get infromation about how many documents we have crawled for a specific event in a specific language.  

The data with manual annotations can be found in `corpus_gold`. The folder follows the same structure as `corpus_clean`.

**Please note: We are still adding and processing data. The respository will be updated regularly.**

## Text representation

Each document is represented in a json file. Each json file contains the text itself (key: text), its headline (key: title) a tokenized version of the text (key: id_token), its original url (key: original_url) and the url used for crawling via Wayback Machine (key: wayback_url).

The documents in the subcorpora Eurovision_Song_Contest_2019 and Eurovision_Song_Contest_2020 have manual annotations for coreference (key: coref) and semantic roles (key: srl).

Documents in the lanugages English, German, French, and Polish are processed with automatic coreference resolution using an integration of Coreferee in Spacy (updates still coming).

Code examples will be added to Explore_data.ipynb.


## Corpus overview

To be updated.

## Corpus collection

### Crawling strategy:

We use Wikidata identifiers of events and participants to access their respective Wikipedia pages in different languages. Each Wikipedia page has a list of sources (often newspaper articles). We crawl these sources via Wayback machine.

**Source events:**

Eurovision Songcontestt 2019
Eurovision Songcontest 2020
Eurovision Songcontest 2021
Germany in the Eurovision Song Contest 2021
Italy in the Eurovision Song Contest 2021
Netherlands in the Eurovision Song Contest
Russia in the Eurovision Song Contest 2021
Ukraine in the Eurovision Song Contest 2021

**Particpants:**
Eurovision Songcontest 2021 (accessed via a Sparql query, see Sparql.ipynb). The resulting Wikidata identifiers can be found in Eurovision_21_participants.txt.



### Languages

We started with the following languages: 'en','nl','it','es','de','fr'

Many source texts are written in a language different from the Wikipedia page. For instance, since the 2021 Eurovision Song contest took place in the Netherlands, many source texts are written in Dutch, even though they are listed as sources on an English or French Wikipedia page.

To identify the actual languages of the texts, we used the python package langdetect (version 1.0.9) (https://pypi.org/project/langdetect/), which turned out to predict languages fairly reliably.

Based on the outcome of the automatic language detection, we exteded our languages with all languages that were predicted. We extended the corpus by crawling all Wikipedia pages in the languages predicted by langdetect.

Limitation: We do not crawl wikipedia pages of people and events if they do not have an entry in English [to be addressed].
