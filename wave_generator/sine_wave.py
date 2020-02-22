from WaveGenerator import WaveGenerator

if __name__ == '__main__':

    save_file = False
    play_sound = True
    repeat = True

    w = WaveGenerator(48000, 2, 2) # Arguments: frame_rate, sample_width, n_channels
    w.generate_sinewave((2000, 0), (2000, 2000), 5) # Arguments: (left_freq, right_freq), (left_volume, right_volume), duration
    
    if save_file:
        w.output_file('./sine.wav')
    
    if play_sound:
        w.play_sound(repeat=repeat)