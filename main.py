import os
import requests


class YandexVkontakte:
    def __init__(self, id_user, access_token_vk, access_token_ya):
        self.id_user = id_user
        self.access_token_vk = access_token_vk
        self.access_token_ya = access_token_ya

    def __get_list_photos(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'access_token': self.access_token_vk,
                  'owner_id': self.id_user,
                  'album_id': 'profile',
                  'v': '5.131',
                  'photo_sizes': 1,
                  'extended': 1}
        dict_photos = requests.get(url, params=params).json()['response']
        list_photo = dict_photos['items']
        finish_list = []
        list_file_name = []
        for photo in list_photo:
            dict_photo = {}
            name_photo = photo['likes']['count']
            file_name = f'{ name_photo}.jpg'
            date_photo = photo['date']
            if file_name in list_file_name:
                file_name = f'{name_photo}_{date_photo}.jpg'
            list_file_name.append(file_name)
            max_size = 0
            url_max_size = ''
            for every_photo in photo['sizes']:
                if max_size < every_photo['height'] * every_photo['width']:
                    max_size = every_photo['height'] * every_photo['width']
                    url_max_size = every_photo['url']
            dict_photo['file_name'] = file_name
            dict_photo['size'] = max_size
            dict_photo['url'] = url_max_size
            dict_photo['date'] = date_photo
            finish_list.append(dict_photo)
        return finish_list

    def upload_photo_yandex(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Authorization': self.access_token_ya,
                   'Content-Type': 'application/json'}
        all_photo = len(self.__get_list_photos())
        progress = 0
        for char_photo in self.__get_list_photos():
            file_name = char_photo['file_name']
            url_photo = char_photo['url']
            params = {'path': f'disk:/vk/{file_name}',
                      'url':  url_photo}
            requests.post(url=url, headers=headers, params=params)
            progress += 1
            print(f'Загружено {progress} из {all_photo} фотографий')


if __name__ == '__main__':
    Korovin = YandexVkontakte(os.getenv('id_korovin'), os.getenv('token_korovin'), os.getenv('token_ya'))
    Korovin.upload_photo_yandex()
