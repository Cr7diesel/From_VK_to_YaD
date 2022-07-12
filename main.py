import requests
from tqdm import tqdm
import json
from datetime import datetime

with open('text.txt') as file:
    token = file.read().strip()


class VkUser:
    url = 'https://api.vk.com/method/photos.get'

    def __init__(self, vk_id, version='5.131', vk_token=token):
        self.vk_token = vk_token
        self.version = version
        self.vk_id = vk_id
        self.params = {'access_token': self.vk_token, 'v': version}

    @staticmethod
    def get_max_size(sizes):
        return max(sizes, key=lambda size: size['height'] * size['width'])

    def get_vk_photo(self):
        result = []
        albums = ['profile', 'saved', 'wall']
        for album in albums:
            params2 = {'owner_id': self.vk_id,
                       'album_id': album,
                       'extended': 1,
                       'photo_sizes': 1,
                       'count': 5}
            response = requests.get(url=self.url, params={**self.params, **params2})
            try:
                photos = response.json()['response']['items']
            except KeyError:
                print(f'Пользователь закрыл доступ к альбому {album} или альбом отсутствует!')
                photos = []
            for photo in tqdm(photos):
                required_size = self.get_max_size(photo['sizes'])
                result.append({'likes': str(photo['likes']['count']), 'url': required_size['url'],
                               'date': str(photo['date']), 'type': required_size['type']})
        return result


class UploadToYaD:
    def __init__(self, ya_token):
        self.ya_token = ya_token
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': f'OAuth {self.ya_token}'}

    def create_folder(self, name):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': name}
        requests.put(url, params=params, headers=self.headers)

    def upload(self, url_file, path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {'url': url_file, 'path': path}
        requests.post(url=url, params=params, headers=self.headers)

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
        with open('about_photo', 'w') as f:
            json.dump(named_photo, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    vk_user_id = VkUser(input('Введите id пользователя: '))
    uploader = UploadToYaD(input('Введите токен ЯндексДиска: '))
    print('Скачиваем фотографии профиля и сохраняем на ЯндексДиск')
    uploader.from_vk_to_yad(vk_user_id)
