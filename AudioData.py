import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack, signal
from matplotlib import lines

class AudioData:
    def __init__(self, id, chunk, rate, n_chunks):
        self.window = signal.hamming(chunk)
        self.chunk = chunk
        self.rate = rate
        self.n_chunks = n_chunks
        
        self.time_line = lines.Line2D([], [])
        self.freq_line = lines.Line2D([], [])
        self.time_xdata = np.arange(0, chunk, 1) / rate
        self.time_ydata = np.zeros(chunk)
        self.freq_xdata = np.arange(1, chunk // 2 + 1, 1) * rate / chunk
        self.freq_ydata = np.zeros(chunk // 2)
        self.spectrogram = []
        self.spec_tdata = np.arange(0, self.n_chunks) * chunk / rate
        self.fig = plt.figure('Device: {}'.format(id))
        self.ax = self.fig.subplots(3, 1)

        self.ax[0].set_title('Waveform')
        self.ax[0].set_xlim(0, chunk / rate)
        self.ax[0].set_ylim(-50000, 50000)
        self.ax[0].add_line(self.time_line)
        self.ax[1].set_title('Frequency')
        self.ax[1].set_xlim(0, rate // 2)
        self.ax[1].set_ylim(0, 1000)
        self.ax[1].add_line(self.freq_line)
        self.ax[2].set_xlim(0, (n_chunks - 1) * chunk / rate)
        self.ax[2].set_ylim(0, rate // 2)
        self.ax[2].set_title('Spectrogram')

    def stft(self, x):
        z = fftpack.fft(x * self.window)
        y = np.abs(z)[1:z.shape[-1] // 2 + 1] * 2 / z.shape[-1]
        return y
    
    def push_data(self, data):
        self.time_ydata = data
        self.freq_ydata = self.stft(data)
        self.spectrogram.append(self.freq_ydata)
        if (len(self.spectrogram) > self.n_chunks):
            self.spectrogram.pop(0)
    
    def update_plot(self, i):
        self.time_line.set_xdata(self.time_xdata)
        self.time_line.set_ydata(self.time_ydata)
        self.freq_line.set_xdata(self.freq_xdata)
        self.freq_line.set_ydata(self.freq_ydata)
        if len(self.spectrogram) == self.n_chunks:
            spec = self.ax[2].pcolormesh(self.spec_tdata, self.freq_xdata,
                                         10 * np.log10(np.array(self.spectrogram).T),
                                         vmin=0, vmax=10 * np.log10(self.rate // 2))
            return self.freq_line, self.time_line, spec
        else:
            return self.freq_line, self.time_line