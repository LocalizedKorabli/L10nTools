import os
import re

import polib

if not os.path.exists('input'):
    os.mkdir('input')
if not os.path.exists('output'):
    os.mkdir('output')

action = input('''
按1进行input/source.po俄语文件分离出output/diff.po
按2进行input/translated.po向input/source.po合并为output/merged.po
''')

source_po = polib.pofile('input/source.po')
if int(action) == 1:
    russian_pattern = re.compile('[а-яА-ЯёЁ]')
    diff_file = polib.POFile()
    for entry in source_po:
        if entry.msgid and russian_pattern.search(entry.msgstr):
            diff_file.append(entry)
        if entry.msgid_plural:
            strs = entry.msgstr_plural
            should_add = False
            for i in range(0, len(strs) - 1):
                if not should_add and russian_pattern.search(strs[i]):
                    should_add = True
            if should_add:
                diff_file.append(entry)
    diff_file.save('output/diff.po')
elif int(action) == 2:
    translated_po = polib.pofile('input/translated.po')
    translation_dict_singular = {entry.msgid: entry.msgstr for entry in translated_po}
    translation_dict_plural: dict[str, list[str]] = {entry.msgid_plural: entry.msgstr_plural for entry in translated_po}
    for entry in source_po:
        if entry.msgid and entry.msgid in translation_dict_singular:
            entry.msgstr = translation_dict_singular[entry.msgid]
        if entry.msgid_plural and entry.msgid_plural in translation_dict_plural:
            entry.msgstr_plural = translation_dict_plural.get(entry.msgid_plural)
    source_po.save('output/merged.po')

input("按回车键退出")
