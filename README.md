# Visualization for Multiple Microphones

## About

Real-time visualization of waveforms, frequency spectrums and spectrograms for multiple input microphones

## Run

Change device IDs in MIC_DEVICE_ID

```
$ python3 multi-microphone.py
```

## Microphone device ID

You can look up microphone device IDs using the following script:

```python
import pyaudio

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
```
