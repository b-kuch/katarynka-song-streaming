from functools import partial


class get_song:
    def __init__(self, file_name, CHUNK_SIZE=1024):
        self.file_obj = open(file_name, 'br')
        self.CHUNK_SIZE = CHUNK_SIZE

    def __enter__(self):
        return iter(partial(self.file_obj.read, self.CHUNK_SIZE), b'')

    def __exit__(self, _type, value, traceback):
        self.file_obj.close()
