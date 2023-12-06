import json
import os

selection_desc = '''
0.比对source.json和translated.json中的对象列表，将后者向前者覆盖为merged.json，并生成diff.json
1.将source.json变为单行后输出到1line.json
'''

if not os.path.exists('input'):
    os.mkdir('input')
if not os.path.exists('output'):
    os.mkdir('output')

selection = input(selection_desc)

with open('input/source.json', 'r', encoding='utf-8') as file:
    source_json = json.load(file)

if selection == "0":
    merged_dict = {}
    diff_dict = {}
    ids_dict = {}
    temp_dict = {}
    if isinstance(source_json, dict):
        if 'IDS' in source_json:
            ids = source_json['IDS']
            if isinstance(ids, dict):
                ids_dict = ids.copy()
        if 'TEMPLATES' in source_json:
            templates = source_json['TEMPLATES']
            if isinstance(templates, dict):
                temp_dict = templates.copy()

    with open('input/translated.json', 'r', encoding='utf-8') as file:
        translated_json = json.load(file)

    ids_dict_remain = ids_dict.copy()
    temp_dict_remain = temp_dict.copy()

    if isinstance(translated_json, dict):
        if 'IDS' in translated_json:
            ids = translated_json['IDS']
            if isinstance(ids, dict):
                for key in ids:
                    if key in ids_dict:
                        ids_dict[key] = ids[key]
                    if key in ids_dict_remain:
                        del ids_dict_remain[key]
        if 'TEMPLATES' in translated_json:
            templates = translated_json['TEMPLATES']
            if isinstance(templates, dict):
                for key in templates:
                    if key in temp_dict:
                        temp_dict[key] = templates[key]
                    if key in temp_dict_remain:
                        del temp_dict_remain[key]

    merged_dict['IDS'] = ids_dict
    merged_dict['TEMPLATES'] = temp_dict

    diff_dict['IDS'] = ids_dict_remain
    diff_dict['TEMPLATES'] = temp_dict_remain

    with open('output/merged.json', 'w', encoding='utf-8') as file:
        json.dump(merged_dict, file, indent=2, ensure_ascii=False)

    with open('output/diff.json', 'w', encoding='utf-8') as file:
        json.dump(diff_dict, file, indent=2, ensure_ascii=False)
elif selection == "1":
    with open('input/source.json', 'r', encoding='utf-8') as file:
        source_json = json.load(file)
    with open('output/1line.json', 'w', encoding='utf-8') as file:
        json.dump(source_json, file, indent=None, separators=(',', ':'), ensure_ascii=False)
