from typing import List

import requests

API_URL: str = 'https://api.deepl.com/v2/translate'


def translate(text: str, to_lang: str, from_lang: str = None, formality: str = 'default') -> str:

    data = {
        'auth_key': '9dad9d05-7f40-21f5-5eac-0e37f4ef6389',
        'target_lang': to_lang,
        'from_lang': from_lang,
        'formality': formality,
        'text': text
    }

    r = requests.get(API_URL, data)

    if r.status_code != 200:
        if r.status_code == 403:
            raise Exception('DeepL API returned an authentication error ' + str(r.status_code))
        else:
            raise Exception('DeepL API returned an error ' + str(r.status_code))

    return r.json()['translations'][0]['text']


def max_texts(texts: List[str], max_chars: int):
    count = 0
    index = 0
    for text in texts:
        if count + len(text) > max_chars:
            return index
        count += len(text)
        index += 1
    return index


def translate_batch(texts: List[str], to_lang: str, from_lang: str = None, formality: str = 'default', verbose: bool = True) -> List[str]:

    # clone the list
    total_texts = len(texts)
    texts = texts.copy()

    translated_texts = []

    while len(texts) > 0:
        if verbose:
            print('\rTranslation... ' + str(len(translated_texts) / total_texts * 100) + '%', end='')

        texts_to_take = max_texts(texts, 1500)

        data = {
            'auth_key': '9dad9d05-7f40-21f5-5eac-0e37f4ef6389',
            'target_lang': to_lang,
            'from_lang': from_lang,
            'formality': formality,
            'text': texts[:texts_to_take]
        }

        texts = texts[texts_to_take:]

        r = requests.get(API_URL, data)

        if r.status_code != 200:
            if r.status_code == 403:
                raise Exception('DeepL API returned an authentication error ' + str(r.status_code))
            else:
                raise Exception('DeepL API returned an error ' + str(r.status_code))

        translated_texts += [translation['text'] for translation in r.json()['translations']]
    return translated_texts
