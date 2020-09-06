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
            raise Exception('DeepL API returned an authentication error '+str(r.status_code))
        else:
            raise Exception('DeepL API returned an error '+str(r.status_code))

    return r.json()['translations'][0]['text']

