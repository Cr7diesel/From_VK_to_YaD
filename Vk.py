import requests
from tqdm import tqdm

token = ''


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
            if response.status_code != 200:
                print('Что-то пошло не так!')
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
