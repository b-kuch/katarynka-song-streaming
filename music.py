from functools import partial

import pyaudio as pyaudio


def gen_header(sample_rate, bits_per_sample, channels, samples):
    datasize = samples * channels * bits_per_sample // 8
    o = bytes("RIFF", 'ascii')  # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4, 'little')  # (4byte) File size in bytes excluding
    # this and RIFF marker
    o += bytes("WAVE", 'ascii')  # (4byte) File type
    o += bytes("fmt ", 'ascii')  # (4byte) Format Chunk Marker
    o += (16).to_bytes(4, 'little')  # (4byte) Length of above format data
    o += (1).to_bytes(2, 'little')  # (2byte) Format type (1 - PCM)
    o += channels.to_bytes(2, 'little')  # (2byte)
    o += sample_rate.to_bytes(4, 'little')  # (4byte)
    o += (sample_rate * channels * bits_per_sample // 8).to_bytes(4, 'little')  # (4byte)
    o += (channels * bits_per_sample // 8).to_bytes(2, 'little')  # (2byte)
    o += bits_per_sample.to_bytes(2, 'little')  # (2byte)
    o += bytes("data", 'ascii')  # (4byte) Data Chunk Marker
    o += datasize.to_bytes(4, 'little')  # (4byte) Data size in bytes
    return o


FORMAT = pyaudio.paInt16
CHUNK = 102400  # 1024
RATE = 44100
bitsPerSample = 16  # 16
CHANNELS = 1
wav_header = gen_header(RATE, bitsPerSample, CHANNELS, CHUNK)

audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, output=True, input_device_index=10,
                    frames_per_buffer=CHUNK)


# def get_song(song_public_id: str):
#     # start Recording
#     def sound():
#         data = wav_header
#         data += stream.read(CHUNK)
#         yield data
#         while True:
#             data = stream.read(CHUNK)
#             yield data
#     return sound()

# def get_song(song_public_id: str):
#     with open('Here Comes A Big Black Cloud!! - Graverobbin.mp3', 'br') as song_file:
#         return iter(partial(song_file.read, 1024), b'')


class get_song:
    def __init__(self, file_name, CHUNK_SIZE=1024):
        self.file_obj = open(file_name, 'br')
        self.CHUNK_SIZE = CHUNK_SIZE

    def __enter__(self):
        return iter(partial(self.file_obj.read, self.CHUNK_SIZE), b'')

    def __exit__(self, _type, value, traceback):
        self.file_obj.close()
