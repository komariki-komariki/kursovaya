import requests
import os

import json
from pprint import pprint
photos_link = []
photos_info = {}
count_dict = {}

class VkPhotos:
    def __init__(self, id_:str):
        self.id_ = id_

    def search_photos(self):
        params = {
            'owner_id': self.id_,
            'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
            'v': '5.131',
            'count': '3',
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '0'}
        response = requests.get('https://api.vk.com/method/photos.get', params=params)
        data = response.json()
        try:
            error_code = data['error']['error_code']
            if data['error']:
                print(f'Ошибка {error_code}, список кодов ошибок по ссылке: https://dev.vk.com/reference/errors')
        except:
            for key, value in data.items():
                count_dict.setdefault(value['count'], params['count'])
                for z in value['items']:
                    photos_info.setdefault(str(z['likes']['count']) + '.jpg', {'size': str(z['sizes'][-1]['type']),
                                                                               "link": str(z['sizes'][-1]['url'])})

class YaUploader:
    def __init__(self, token: str):
        self.token = token
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                   'Authorization': f'OAuth {self.token}'}
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def create_folder(self, path):
        """Создание папки. \n path: Путь к создаваемой папке."""
        requests.put(f'{self.url}?path={path}', headers=self.headers)

    def upload(self, loadfile, savefile, replace=False):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {self.token}'}
        result = requests.get(f'{upload_url}/upload?path={savefile}&overwrite={replace}', headers=headers).json()
        with open(loadfile, 'rb') as f:
            try:
                requests.put(result['href'], files={'file':f})
                print(f'Файл {savefile} успешно сохранен')
            except KeyError:
                print(result)
def perebor():
    for count_profil, count_req in count_dict.items():
        a = int(count_profil)
        b = int(count_req)
    if a > b:
        i = b
    else:
        i = a
    # bar = IncrementalBar('Загрузка', max = i)
    for k, v in photos_info.items():
        uploader = YaUploader(token)
        uploader.create_folder(id_)
        img_data = requests.get(v['link']).content
        with open(k, 'wb') as handler:
            handler.write(img_data)
        uploader = YaUploader(token)
        uploader.upload(k, f'/{id_}/{str(k)}')
        photos_link.append({'name': str(k), 'size': str(v['size'])})
        os.remove(k)
        # bar.next()
        # bar.finish

if __name__ == '__main__':
    id_ = '60966949'
    token = ''
    res = VkPhotos(id_)
    rez = res.search_photos()
    perebor()
    print(count_dict)
