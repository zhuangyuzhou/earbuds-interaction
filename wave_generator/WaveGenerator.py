import wave
import numpy as np
import pyaudio

class WaveGenerator:
    def __init__(self, frame_rate, sample_width, n_channels):
        if n_channels not in [1, 2]:
            raise ValueError('n_channels should be either 0 or 1')
        if sample_width not in [2]:
            raise ValueError('Only sample_width=2 (16 bits) is supported for now')
        self.frame_rate = frame_rate
        self.sample_width = sample_width
        self.n_channels = n_channels
    
    def generate_sinewave(self, freqs, volumes, duration):
        if self.n_channels == 1: # Mono
            x = np.linspace(0, duration, num=duration * self.frame_rate)
            y = np.sin(2 * np.pi * freqs[0] * x) * volumes[0]
        elif self.n_channels == 2: # Stereo
            x = np.linspace(0, duration, num=duration * self.frame_rate)
            y_left = np.sin(2 * np.pi * freqs[0] * x) * volumes[0]
            y_right = np.sin(2 * np.pi * freqs[1] * x) * volumes[1]
            y = np.zeros(2 * len(x))
            y[::2] = y_left
            y[1::2] = y_right
        if self.sample_width == 2:
            self.data = y.round().astype(np.int16)
    
    def output_file(self, filename):
        data_bytes = self.data.tobytes()
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.n_channels)
        wf.setframerate(self.frame_rate)
        wf.setsampwidth(self.sample_width)
        wf.setcomptype('NONE','not compressed')
        wf.writeframes(data_bytes)
        print('File saved as "{}"'.format(filename))

    def play_sound(self, chunk_size=1024, repeat=False):
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(self.sample_width),
                        channels=self.n_channels,
                        rate=self.frame_rate,
                        output=True)
        
        print('Strart playing')
        if repeat:
            while True:
                stream.write(self.data)
        else:
            stream.write(self.data)
            print('Done playing')
        
        stream.stop_stream()
        stream.close()
        p.terminate()
