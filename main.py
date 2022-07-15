from Photo import Photo
from VK_API import VK_API
from Yandex_API import Yandex_API


def download_ph():
    ya_token = input('YandexDisk token:')
    id = input('VK user id:')
    quantity = input('Number of photos to upload: ')
    vk_api = VK_API()
    ya_api = Yandex_API(ya_token)
    ya_api.upload(id, vk_api.get_photos(id, int(quantity)))


if __name__ == '__main__':
    download_ph()
