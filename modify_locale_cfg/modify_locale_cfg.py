import xml.etree.ElementTree as ETree

input("确保本程序与locale_config.xml位于同一目录下，按回车键继续。")
tree = ETree.parse('locale_config.xml')
tree_copy = ETree.parse('locale_config.xml')
root = tree.getroot()

executed = False
for lang_elem in root.findall('.//lang'):
    accept_lang = lang_elem.get('acceptLang')
    if accept_lang == 'ru':
        lang_elem.set('fonts', 'CN')
        executed = True

tree.write('locale_config.xml')
tree_copy.write('locale_config.xml.old')

print(
    "操作成功。原文件已备份为locale_config.xml.old" if executed else "操作失败，请尝试向https://github.com/Nova-Committee/Korabli-LESTA-L10N报告。")
input("按回车键退出。")
