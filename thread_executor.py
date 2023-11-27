import os
import tqdm
try:
    import yt_dlp as youtube_dl
except:
    os.system("""pip install https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz""")
    import yt_dlp as youtube_dl
import json
import copy
import librosa
import numpy as np
from time import time, sleep
from keras.utils import to_categorical
import json
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def get_segment_frequencies(audio_file_path, segment_size = 2210):
    audio_file_path, encoding = audio_file_path
    # Step 1: Read the audio file
    audio_data, sample_rate = librosa.load(audio_file_path, sr=None)

    # Step 2: Resample to a fixed sample rate (22.1kHz)
    target_sample_rate = 22100
    audio_data = librosa.resample(y = audio_data, orig_sr = sample_rate, target_sr = target_sample_rate)

    # Step 3: Divide the audio file into multiple segments
    num_segments = len(audio_data) // segment_size
    audio_data = audio_data[:num_segments * segment_size]  # Truncate to an integer number of segments
    segments = audio_data.reshape(num_segments, segment_size)

    # Step 4: Identify the frequency of each segment
    frequencies = []
    for segment in segments:
        # Perform Fourier Transform to get the frequency domain representation
        spectrum = np.abs(np.fft.fft(segment))
        # Get the dominant frequency (peak) in the spectrum
        dominant_frequency = np.argmax(spectrum)
        # Convert the dominant frequency bin to Hz
        frequency = dominant_frequency * (target_sample_rate / segment_size)
        frequencies.append(frequency)
    # Step 5: Return the frequencies of all segments as a list
    return frequencies, encoding

if __name__ == '__main__':
    input_dir = "vocals_main_mp3_by_raga_chunks"
    all_classes = os.listdir(input_dir)
    num_classes = len(all_classes)
    start = time()
    data = []
    for class_name in all_classes:
        folder_path = os.path.join(input_dir, class_name)
        class_index = int(class_name) - 1
        one_hot_encoding = tuple(int(el) for el in to_categorical(class_index, num_classes))
        class_data = [(os.path.join(folder_path, file_name), one_hot_encoding) for file_name in os.listdir(folder_path)]
        data += class_data
    # data = data[1000:1100]
    with ThreadPoolExecutor(max_workers=3) as exe:
        content = list(tqdm.tqdm(exe.map(get_segment_frequencies, data), total=len(data)))
        json.dump(content, open('loaded_data.json', 'w'))
    print(f"Time Taken: {time() - start}")


