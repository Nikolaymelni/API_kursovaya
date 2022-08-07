import requests
import json
import datetime
import configparser


class VkUser:
    url = 'https://api.vk.com/method/'
    config_vk = configparser.ConfigParser()
    config_vk.read("tokens.ini")
    token_vk = config_vk["vk"]["token"]
    #token_vk = (input('Введите токен ВК: '))
    params = {
        'access_token': token_vk,
        'v': '5.131'
    }


    def __init__(self, user_id=None):

        self.info_foto_list = []
        if user_id is not None:
            self.user_id = user_id
        else:
            self.user_id = requests.get(self.url + 'users.get', self.params).json()['response'][0]['id']


    def photos_get(self, counter):
        photos_get_url = self.url + 'photos.get'
        counter = int(input('Количество фотографий для скачивания: '))
        photos_get_params = {
            'owner_id': self.user_id,
            'album_id': input('Где хранятся нужные фотографии? Ответ на латинице("wall" - стена, '
                     '"profile" - профиль, "saved" - сохраненные, "album" - альбом): '),
            'extended': '1',
            'photo_sizes': '1',
            'count': counter,
            'rev': '1'
            }
        res = requests.get(photos_get_url, params={**self.params, **photos_get_params})
        res.raise_for_status()
        info_foto_dict = res.json()
        print(f'Информация получена')
        return info_foto_dict

    def conv_dict_list(self, information_dict):
        foto_list = []
        for dict_ in information_dict['response']['items']:
            dict_foto = {}
            dict_foto['date'] = datetime.datetime.fromtimestamp(dict_['date']).strftime('%d.%m.%Y %H.%M.%S')
            dict_foto['likes'] = dict_['likes']['count']
            example = 0
            for var_url in dict_['sizes']:
                size = var_url['height'] * var_url['width']
                if size > example:
                    example = size
                    dict_foto['url'] = var_url['url']
                    dict_foto['size'] = var_url['type']
            foto_list.append(dict_foto)

        info_foto_list = []
        num = len(foto_list)
        for i in range(num - 1):
            dict_ = foto_list.pop()
            for string in foto_list:
                if string['likes'] == dict_['likes']:
                    dict_['file-name'] = '(' + str(dict_['date']) + ')' + str(dict_['likes']) + '.jpg'
                    break
                else:
                    dict_['file-name'] = str(dict_['likes']) + '.jpg'

            info_foto_list.append(dict_)

        last_dict = foto_list.pop()
        last_dict['file-name'] = str(last_dict['likes']) + '.jpg'
        info_foto_list.append(last_dict)
        print(f'Информация конвертирована в список')
        return info_foto_list

    def create_list_with_requested_information(self, count=None):
        self.info_foto_list = self.conv_dict_list(self.photos_get(count))
        return

    def create_json(self, name=None):
        if name is not None:
            name_file = name
        else:
            name_file = 'output'
        info_list = self.info_foto_list
        for string in info_list:
            del string['likes'], string['date'], string['url']
        with open(name_file + '.json', "w") as f:
            json.dump(info_list, f, ensure_ascii=False, indent=4)
        print(f'Создан файл с информацией о полученных фото')
        return info_list
