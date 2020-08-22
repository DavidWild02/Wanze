import pyaudio
import wave
import audioop
from collections import deque
import math

class Recorder:
    def __init__(self, config):
        try:
            self.format = config['format']
            self.channels = config['channels']
            self.rate= config['rate']
            self.chunk = config['chunk']
            self.silence_limit = config['silence_limit']
            self.threshold = config['threshold']
            self.device_index = config['device_index']
            self.recordings_max = config['recordings']
        except KeyError as e:
            print('KeyError: The following config-variable, was not specified:' + e.args[0])
            exit()

        self.audio = pyaudio.PyAudio()
        self.data = []
        self.recordings = 0


    def __iter__(self):
        stream = self.audio.open(format=self.format,
                            channels=self.channels,
                            rate=self.rate,
                            input=True,
                            frames_per_buffer=self.chunk,
                            input_device_index=self.device_index)

        self.data = []
        cur_data = b''
        slid_win = deque(maxlen=int(self.silence_limit * self.rate / self.chunk))
        started = False
        print('Listening...')

        while (self.recordings < self.recordings_max):
            cur_data = stream.read(self.chunk)
            slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
            if any([x > self.threshold for x in slid_win]):
                if not started:
                    print('Started recording')
                    started = True
                self.data.append(cur_data)
            elif started == True:
                print('Finished recording')
                self.recordings += 1
                self.save_audio_data()
                yield

                self.data = []
                cur_data = b''
                slid_win = deque(maxlen=int(self.silence_limit * self.rate / self.chunk))
                started = False
                print('Listening...')

        print('All recordings were made')



    def save_audio_data(self):
        wavefile = wave.open('temp.wav', 'wb')
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self.audio.get_sample_size(self.format))
        wavefile.setframerate(self.rate)
        wavefile.writeframes(b''.join(self.data))
        wavefile.close()