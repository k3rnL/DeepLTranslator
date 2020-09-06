import os
import re
import xml.etree.ElementTree as ET
from sys import argv
from typing import List


from deepl import translate


def get_xliff_files() -> List[str]:
    xliff_files = []
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if name.endswith('.xliff'):
                xliff_files += [os.path.join(root, name)]

    return xliff_files


def clean_text(raw):
    clea_nb = re.compile('<g.*?>')
    clean_e = re.compile('</g>')
    clean_txt = re.sub(clea_nb, '', raw)
    clean_txt = re.sub(clean_e, '', clean_txt)
    return clean_txt


formality = 'default'

for file in [f for f in get_xliff_files() if 'translated' not in f]:
    out_file = file[file.rindex(os.sep) + 1:]
    if os.path.exists(os.path.join('.' + os.sep + 'translated', out_file)):
        print('File already translated: ' + out_file)
        continue

    input_text = clean_text(open(file, 'r', encoding='utf-8').read())

    root = ET.fromstring(input_text)
    body = root[0][1]
    units = list(body)

    source_language = root[0].attrib["source-language"]
    target_language = root[0].attrib["target-language"]

    print('Opening ' + file + ', translate from ' + source_language.upper() + ' to ' + target_language.upper())

    for unit in units:
        print('\rTranslation... ' + str(int(units.index(unit) / len(units) * 100)) + '%', end='')
        try:
            if unit[0].text is not None and unit[1].attrib["state"] == "needs-translation":
                unit[1].text = translate(unit[0].text, from_lang=source_language, to_lang=target_language, formality=formality)
        except Exception as e:
            print("Error during translation because:" + str(e))
            continue

    print('\rTranslation... 100%')
    replaced = ET.tostring(root, encoding="unicode")\
        .replace("<ns0:", "<")\
        .replace("</ns0:", "</")\
        .replace("xmlns:ns0", "xmlns")

    open('./translated/' + out_file, 'w', encoding='utf-8').write(replaced)
    print('Translated file written: ' + './translated/' + out_file)
    print()
