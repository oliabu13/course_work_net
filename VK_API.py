import requests
from Photo import Photo


class VK_API:
    base_url = "https://api.vk.com/method/"

    def __init__(self):
        self.token = ' '
        self.version = '5.131'

    @staticmethod
    def find_largest(sizes):
        ph_sizes = ['x', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm', 's']
        for photo in ph_sizes:
            for size in sizes:
                if size['type'] == photo:
                    return size

    def get_photos(self, id, quantity=5):
        url = self.base_url + 'photos.get'
        resp = requests.get(url, params={
            'access_token': self.token,
            'v': self.version,
            'owner_id': id,
            'album_id': 'profile',
            'photo_sizes': 1,
            'extended': 1
        }).json().get('response').get('items')

        return sorted([Photo(photo.get('date'),
                             photo.get('likes')['count'],
                             self.find_largest(photo.get('sizes'))) for photo in resp],
                      key=lambda p: p.maxsize, reverse=True)[:quantity]
