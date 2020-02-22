import threading
import queue

import numpy as np
import pyaudio
from matplotlib import animation
import tkinter as tk

from AudioData import AudioData

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 1024
N_CHUNKS = 100

'''
# Get device id:
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
'''
MIC_DEVICE_ID = [1, 2]

# Callback function for pyaudio streams
def stream_callback(queue, rdy_event):
    def callback(in_data, frame_count, time_info, status):
        queue.put(np.frombuffer(in_data, np.dtype('<i2')))
        rdy_event.set()
        return (None, pyaudio.paContinue)
    return callback

# Queue processing thread
def queue_processor(queue, rdy_event, stream, audio_data):
    while stream.is_active():
        rdy_event.wait(timeout=10000)
        data = None
        while not queue.empty():
            data = queue.get()
        if data is not None:
            audio_data.push_data(data)
        rdy_event.clear()

# On close figure window
def on_close(stream, p, id):
    def destroy_all(ev):
        stream.stop_stream()
        stream.close()
        p.terminate()
        print('Device {}: done recording'.format(id))
    return destroy_all

if __name__ == '__main__':
    
    queues = [queue.Queue() for _ in range(len(MIC_DEVICE_ID))]
    rdy_events = [threading.Event() for _ in range(len(MIC_DEVICE_ID))] # Signal data is ready
    
    for i, id in enumerate(MIC_DEVICE_ID):
        audio_data = AudioData(id, CHUNK, RATE, N_CHUNKS) # Storing data for processing and visualization
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True, input_device_index=id,
                    frames_per_buffer=CHUNK,
                    stream_callback=stream_callback(queues[i], rdy_events[i]))
        
        # Start animation
        ani = animation.FuncAnimation(audio_data.fig, audio_data.update_plot,
                                      frames=1, interval=30, blit=True)
        
        t = threading.Thread(target=queue_processor, args=(queues[i], rdy_events[i], stream, audio_data))
        t.setDaemon(True)
        
        print('Device {}: start recording'.format(id))
        stream.start_stream()
        t.start()
        audio_data.fig.canvas.mpl_connect('close_event', on_close(stream, p, id))
        audio_data.fig.tight_layout()
        audio_data.fig.show()
        
    root = tk.Tk()
    root.mainloop()
        
        