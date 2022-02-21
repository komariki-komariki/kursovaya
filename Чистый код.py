import requests
from pprint import pprint

photos_info = {}
params = {
    'owner_id': '5612706',
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
    for x, y in data.items():
        # print(y['count']) # количество фотографий в профиле
        for z in y['items']:
            photos_info.setdefault(str(z['likes']['count']) + '.jpg', {'size': str(z['sizes'][-1]['type']), "link": str(z['sizes'][-1]['url'])})

pprint(photos_info)