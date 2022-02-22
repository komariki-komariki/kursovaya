import requests
import os
from pprint import pprint
# _id = str(input('Введите id: '))
# photos_count = str(input(f'Введите количество фотографий для загрузки, количество фотографий в профиле - {bv}: '))
photos_link = []
photos_info = {}

class VkPhotos:
    def __init__(self, id_:str):
        self.id_ = id_

    def search_photos(self):
        params = {
            'owner_id': self.id_,
            'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
            'v': '5.131',
            'count': '10',
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
                # print(value['count']) # количество фотографий в профиле
                for z in value['items']:
                    photos_info.setdefault(str(z['likes']['count']) + '.jpg', {'size': str(z['sizes'][-1]['type']),
                                                                               "link": str(z['sizes'][-1]['url'])})

class YaUploader:
    def __init__(self, token: str):
        self.token = token
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                   'Authorization': f'OAuth {self.token}'}
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def create_folder(self, path): # РАБОТАЕТ
        """Создание папки. \n path: Путь к создаваемой папке."""
        requests.put(f'{self.url}?path={path}', headers=self.headers)

    # def upload(self, loadfile, replace=False):
    #     savefile = "1.jpg"
    #     upload_url = 'https://cloud-api.yandex.net/v1/disk/resources'
    #     headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {self.token}'}
    #     result = requests.get(f'{upload_url}/upload?path={savefile}&overwrite={replace}', headers=headers).json()
    #     with open(loadfile, 'rb') as f:
    #         try:
    #             requests.put(result['href'], files={'file':f})
    #             print(f'Файл {savefile} успешно сохранен')
    #         except KeyError:
    #             print(result)

if __name__ == '__main__':
    id_ = '758655'
    token = ''
    uploader = YaUploader(token)
    # uploader.upload('https://sun9-23.userapi.com/c302701/u758655/150063596/z_654b532d.jpg')
    result = uploader.create_folder('folder')
    res = VkPhotos(id_)
    rez = res.search_photos()
    print(photos_info)

def perebor():
    for k, v in photos_info.items():
        print(k) # Название файла для загрузки
        print(v['size']) # размер фото
        print(v['link']) # ссылка на скачивание
        photos_link.append({'name': str(k), 'size': str(v['size'])}) # создан список для сохранения в json-файл

perebor()
print(photos_link)

# Загрузка фото из интернета
# url = 'https://sun9-23.userapi.com/c302701/u758655/150063596/z_654b532d.jpg'
# img_data = requests.get(url).content
# with open('image_name.jpg', 'wb') as handler:
#     handler.write(img_data)