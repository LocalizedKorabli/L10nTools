import os
import re

import polib


def compare_lists(list0: list[str], list1: list[str]) -> bool:
    if len(list0) != len(list1):
        return False
    for index in range(len(list0)):
        if list0[index] == list1[index]:
            continue
        else:
            return False
    return True


if not os.path.exists('input'):
    os.mkdir('input')
if not os.path.exists('output'):
    os.mkdir('output')

action = input('''
按1进行input/source.po俄语文件分离出output/diff.po
按2进行input/translated.po向input/source.po合并为output/merged.po
按3进行input/old.po和input/new.po进行比对，并输出差异update_diff.po
''')

if int(action) == 1:
    source_po = polib.pofile('input/source.po')
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
    source_po = polib.pofile('input/source.po')
    translated_po = polib.pofile('input/translated.po')
    translation_dict_singular = {entry.msgid: entry.msgstr for entry in translated_po}
    translation_dict_plural: dict[str, list[str]] = {entry.msgid_plural: entry.msgstr_plural for entry in translated_po}
    for entry in source_po:
        if entry.msgid and entry.msgid in translation_dict_singular:
            entry.msgstr = translation_dict_singular[entry.msgid]
        if entry.msgid_plural and entry.msgid_plural in translation_dict_plural:
            entry.msgstr_plural = translation_dict_plural.get(entry.msgid_plural)
    source_po.save('output/merged.po')
elif int(action) == 3:
    new_po = polib.pofile('input/new.po')
    old_po = polib.pofile('input/old.po')
    o_dict_singular = {entry.msgid: entry.msgstr for entry in old_po}
    o_dict_plural: dict[str, list[str]] = {entry.msgid_plural: entry.msgstr_plural for entry in old_po}
    diff_add_file = polib.POFile()
    diff_change_file = polib.POFile()
    for entry in new_po:
        if entry.msgid:
            if entry.msgid not in o_dict_singular:
                diff_add_file.append(entry)
            elif entry.msgstr != o_dict_singular[entry.msgid]:
                diff_change_file.append(entry)

        if entry.msgid_plural:
            if entry.msgid_plural not in o_dict_plural:
                diff_add_file.append(entry)
            elif not compare_lists(o_dict_plural[entry.msgid_plural], entry.msgstr_plural):
                diff_change_file.append(entry)

    diff_add_file.save('output/diff_add.po')
    diff_change_file.save('output/diff_change.po')

input("按回车键退出")
