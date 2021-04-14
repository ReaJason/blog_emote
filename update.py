#code=utf-8
import os
import json
from collections import OrderedDict

emojiCDN = 'https://cdn.jsdelivr.net/gh/ReaJason/blog_emote/emote/'
readme_list = ["```", f"emojiCDN: {emojiCDN}"]
emojiMaps = OrderedDict()
list_dir = os.listdir()
root_path = os.path.split(os.path.abspath(__file__))[0]
emote_path = os.path.join(root_path, 'emote')
file_list = os.listdir(emote_path)
for file in file_list:
    file_name = file.split('.')[0]
    emojiMaps[file_name] = file
readme_list.append(f"emojiMaps: {json.dumps(dict(emojiMaps), indent=4, separators=(', ', ': '), ensure_ascii=False)}")
readme_list.append("```")
with open(os.path.join(root_path, 'README.md'), 'w', encoding='utf-8') as f:
    f.write("\n".join(readme_list))

