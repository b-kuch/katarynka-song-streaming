import os.path
from functools import partial

CHUNK_SIZE = 1024 * 256

CATALOG_PATH = r'/songs/'


def get_song2(file_name):
    file_path = CATALOG_PATH + file_name
    with open(file_path, 'br') as f:
        return f.read()


def file_size(file_name):
    file_path = CATALOG_PATH + file_name
    return os.path.getsize(file_path)


class get_song:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_path = CATALOG_PATH + file_name
        self.file_obj = open(self.file_path, 'br')

    def __enter__(self):
        return iter(partial(self.file_obj.read, CHUNK_SIZE), b'')

    def __exit__(self, _type, value, traceback):
        self.file_obj.close()
