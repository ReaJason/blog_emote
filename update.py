#code=utf-8
import os
import json
import requests
from collections import OrderedDict

base_url = "https://api.bilibili.com/x/emote/user/panel/web?business=reply"
emojiCDN = 'https://cdn.jsdelivr.net/gh/ReaJason/blog_emote/emote/'

base_path = os.path.dirname(os.path.realpath(__file__))
emote_path = os.path.join(base_path, 'emote')

readme_list = ["```", f"emojiCDN: {emojiCDN}"]
emojiMaps = OrderedDict()

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                    "(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78"
}

if not os.path.exists(emote_path):
    os.mkdir(emote_path)

response_json = requests.get(base_url, headers=headers).json()
emote_packages = response_json['data']['packages']
for emote_package in emote_packages:
    if emote_package['text'] == '颜文字':
        continue
    emote_list = emote_package['emote']
    for emote in emote_list:
        gif_url = emote.get('gif_url')
        if gif_url:
            file_name = f'{emote["text"]}.gif'
            emojiMaps[emote["text"]] = file_name
            with open(os.path.join(emote_path, file_name), 'wb') as f:
                content = requests.get(gif_url).content
                f.write(content)
        else:
            png_url = emote.get('url')
            file_name = f'{emote["text"]}.png'
            emojiMaps[emote["text"]] = file_name
            with open(os.path.join(emote_path, file_name), 'wb') as f:
                content = requests.get(png_url).content
                f.write(content)
readme_list.append(f"emojiMaps: {json.dumps(dict(emojiMaps), indent=4, separators=(', ', ': '), ensure_ascii=False)}")
readme_list.append("```")
with open(os.path.join(base_path, 'README.md'), 'w', encoding='utf-8') as f:
    f.write("\n".join(readme_list))

