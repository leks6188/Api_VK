import requests
import sys
import json
from tqdm import trange

class VK:
    def __init__(self, token_YA, user_id, version='5.131', count_foto = 5):
        self.token_VK = #'ЗДЕСЬ ДОЛЖЕН БЫТЬ ТОКЕН "ВКОНТАКТЕ"'
        self.id = user_id
        self.version = version
        self.token_YA = token_YA
        self.params = {'access_token': self.token_VK, 'v':self.version}
        self.headers_ya = {'Authorization': token_YA }
        self.count_foto = count_foto
        self.url_zaprosa = 'https://cloud-api.yandex.net/v1/disk/resources/upload'

    def users_photos(self):
        params1 = {'path': 'VKphotos'}
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        responce = requests.get(url, params = params1, headers = self.headers_ya)

        if responce.status_code == 200:
            print('Что-то пошло не так.. Такая папка уже существует!')
            sys.exit()
        else:
            requests.put(url, params=params1, headers = self.headers_ya)

        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id, 'album_id': 'profile', 'extended':'1','photo_sizes':'1'}
        response = requests.get(url, params={**self.params, **params})

        all_photos = response.json()
        info_json = []

        if all_photos['response']['count'] > self.count_foto:
            CNT = self.count_foto
        else:
            CNT = (all_photos['response']['count'])

        for item in trange(CNT, desc = 'Идёт процесс загрузки..'):
            likes = all_photos['response']['items'][item]['likes']['count']
            url_foto = all_photos['response']['items'][item]['orig_photo']['url']
            date = all_photos['response']['items'][item]['date']
            format = (url_foto.split('?')[0].split('.'))[-1]
            file = requests.get(url_foto)
            filename = f'{likes}_{date}.{format}'
            height = str(all_photos['response']['items'][item]['orig_photo']['height'])
            width = str(all_photos['response']['items'][item]['orig_photo']['width'])
            info_json.append({'file_name': filename, "size": height+'/'+width})

            params_ya = {"path": f'VKphotos/{filename}'}
            responce = requests.get(self.url_zaprosa, params=params_ya, headers=self.headers_ya)
            url_upload = responce.json()['href']
            requests.put(url_upload, files = {'file': file.content })

        params_ya = {"path": f'VKphotos/information.json'}
        responce = requests.get(self.url_zaprosa, params=params_ya, headers=self.headers_ya)
        url_upload = responce.json()['href']
        requests.put(url_upload, files={'file':json.dumps(info_json)})


user_id = '390026822'
token_Ya = 'OAuth..' #Токен ЯндексДиска
vk = VK(token_Ya, user_id)
vk.users_photos()

