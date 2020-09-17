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


def translate_batch(texts: List[str], to_lang: str, from_lang: str = None, formality: str = 'default', verbose: bool = True) -> List[str]:

    # clone the list
    total_texts = len(texts)
    texts = [texts]

    translated_texts = []

    while len(texts) > 50:
        if verbose:
            print('\rTranslation... ' + str(len(translated_texts) / total_texts * 100) + '%', end='')

        data = {
            'auth_key': '9dad9d05-7f40-21f5-5eac-0e37f4ef6389',
            'target_lang': to_lang,
            'from_lang': from_lang,
            'formality': formality,
            'text': texts[:50]
        }

        texts = texts[50:]

        r = requests.get(API_URL, data)

        if r.status_code != 200:
            if r.status_code == 403:
                raise Exception('DeepL API returned an authentication error ' + str(r.status_code))
            else:
                raise Exception('DeepL API returned an error ' + str(r.status_code))

        translated_texts += [translation.text for translation in r.json()['translations']]
    return translated_texts
