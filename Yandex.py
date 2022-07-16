import requests
from tqdm import tqdm
import json
from datetime import datetime


class UploadToYaD:
    def __init__(self, ya_token):
        self.ya_token = ya_token
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': f'OAuth {self.ya_token}'}

    def create_folder(self, name):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': name}
        res = requests.put(url, params=params, headers=self.headers)
        if res.status_code != 201:
            print('Папка не создана')

    def upload(self, url_file, path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {'url': url_file, 'path': path}
        response = requests.post(url=url, params=params, headers=self.headers)
        if response.status_code != 202:
            print('Ошибка агрузки фотографий ')

    def from_vk_to_yad(self, vk_user):
        folder_name = 'foto_from_vk'
        self.create_folder(folder_name)
        photos = vk_user.get_vk_photo()
        names = []
        named_photo = []
        for photo in tqdm(photos):
            if photo['likes'] not in names:
                name = photo['likes']
            else:
                dt = datetime.fromtimestamp(int(photo['date']))
                name = f"{photo['likes']}_{dt.year}_{dt.month}_{dt.day}"
            names.append(name)
            path = folder_name + '/' + name
            self.upload(photo['url'], path)
            named_photo.append({'file_name': name, 'size': photo['type']})
        with open('about_photo.json', 'w') as f:
            json.dump(named_photo, f, ensure_ascii=False, indent=2)
