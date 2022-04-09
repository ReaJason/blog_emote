# code=utf-8
import os
import json
import requests
from collections import OrderedDict

base_url = "https://api.bilibili.com/x/emote/user/panel/web?business=reply"
emojiCDN = 'https://cdn.jsdelivr.net/gh/ReaJason/blog_emote/emote'

base_path = os.path.dirname(os.path.realpath(__file__))
emote_path = os.path.join(base_path, 'emote')

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78"
}


def make_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def get_image_name(text, img_url):
    return f"{text}.{img_url.split('/')[-1].split('.')[-1]}"


def save_img(path, url):
    with open(path, 'wb') as f:
        content = requests.get(url).content
        f.write(content)


def run():
    make_dir(emote_path)
    response_json = requests.get(base_url, headers=headers).json()
    emote_packages = response_json['data']['packages']
    for emote_package in emote_packages:
        emote_config_list = []
        if emote_package['text'] == '颜文字':
            continue
        pacPath = os.path.join(emote_path, emote_package['text'])
        make_dir(pacPath)

        # 保存 tab 图片
        tab_img_url = emote_package['url']
        tab_img_name = get_image_name(emote_package['text'], tab_img_url)
        save_img(os.path.join(emote_path, tab_img_name), tab_img_url)

        emote_list = emote_package['emote']
        for emote in emote_list:
            img_url = emote.get('gif_url', emote['url'])
            img_name = get_image_name(emote['text'], img_url)
            save_img(os.path.join(pacPath, img_name), img_url)
            emote_config_list.append({
                "src": f"{emojiCDN}/{emote_package['text']}/{img_name}",
                "name": f"@{emote['text']}",
                "reg": '@' + emote["text"].replace("[", "\\[").replace("]", "\\]")
            })
        with open(os.path.join(base_path, f'{emote_package["text"]}.json'), 'w', encoding='utf-8') as f:
            json.dump(emote_config_list, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    run()

    # readme_list.append(
    #     f"emojiMaps: {json.dumps(dict(emojiMaps), indent=4, separators=(', ', ': '), ensure_ascii=False)}")
    # readme_list.append("```")
    # with open(os.path.join(base_path, 'README.md'), 'w', encoding='utf-8') as f:
    #     f.write("\n".join(readme_list))
