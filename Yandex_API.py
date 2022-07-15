import requests
import json
import datetime
from datetime import datetime
from tqdm import tqdm
from time import sleep


class Yandex_API:

    def __init__(self, token: str):
        self.auth = f'OAuth {token}'

    @staticmethod
    def file_name(photos):
        for photo in photos:
            photo.name = str(photo.likes)
            if [p.likes for p in photos].count(photo.likes) > 1:
                photo.name += '_' + str(photo.date)
            photo.name += '.jpg'

    @staticmethod
    def folder_name(new_folder, exist_folders):
        if new_folder not in exist_folders:
            return new_folder
        n = 1
        new_folder += '_' + str(n)
        while new_folder in exist_folders:
            new_folder = new_folder.replace('_' + str(n), '_' + str(n + 1))
            n += 1
        return new_folder

    def get_folders(self):
        return [p['name'] for p in (requests.get("https://cloud-api.yandex.net/v1/disk/resources",
                                                 params={"path": '/'},
                                                 headers={"Authorization": self.auth})
                                    .json().get('_embedded').get('items')) if p['type'] == 'dir']

    def create_folder(self, folder_name):
        resp = requests.put("https://cloud-api.yandex.net/v1/disk/resources",
                            params={"path": '/' + folder_name},
                            headers={"Authorization": self.auth})
        if resp.status_code == 200:
            return resp.ok
        else:
            print('Что-то пошло не так')
        print(f'Имя папки: "{folder_name}":' + str(resp.status_code))
        return resp.ok

    def upload(self, id, photos):
        upload_folder = self.folder_name(id, self.get_folders())
        self.file_name(photos)
        if self.create_folder(upload_folder):
            log_result = []
            for photo in photos:
                response = requests.post("https://cloud-api.yandex.net/v1/disk/resources/upload",
                                         params={"path": '/' + upload_folder + '/' + photo.name,
                                                 "url": photo.url},
                                         headers={"Authorization": self.auth})
                if response.status_code == 202:
                    print(f'Фото "{photo.name}" загружено')
                    log_result.append({"file_name": photo.name, "size": photo.size_type})
                else:
                    print(f'Не получилось загрузить фото "{photo.name}": '
                          f'{response.json().get("message")}. Статус кода: {response.status_code}')
                photos_list = list(photos)
                for _ in tqdm(len(photos_list)):
                    sleep(0.2)
            with open(f'{id}_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}_files.json', "w") as f:
                json.dump(log_result, f, ensure_ascii=False, indent=2)
