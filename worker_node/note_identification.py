# %%
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import matplotlib.pyplot as plt
import librosa
import os
from librosa import display as librosadisplay
import logging
import math
import statistics
import sys
from IPython.display import Audio, Javascript
from scipy.io import wavfile
from scipy import signal
from base64 import b64decode
from pydub import AudioSegment
from time import time
import heapq
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
#print("librosa: %s" % librosa.__version__)
import sys
MAX_ABS_INT16 = 2147483647
# Extract the maximum absolute value from the int16_info tuple


# %%
class note_identification:
    def __init__(self, window_size = 30):
        self.model = hub.load("spice_model")
        self.sample_rate = 16000
        self.window_size = window_size
        self.reference_ratios = [1, 16/15, 9/8, 6/5, 5/4, 4/3, 45/32, 3/2, 8/5, 5/3, 16/9, 15/8, 2]
        self.MAX_ABS_INT16 = 2147483647
        # Constants taken from https://tfhub.dev/google/spice/2
        self.PT_OFFSET = 25.58
        self.PT_SLOPE = 63.07
        self.FMIN = 10.0
        self.BINS_PER_OCTAVE = 12.0
        self.note_names = ["S", "R1", "R2/G1", "R3/G2", "G3", "M1", "M2", "P", "D1", "D2/N1", "N2", "N3","S-next"]
        
    def load_audio_file(self, filename): # takes filename as input and returns model input as output
        os.system("")
        print(filename)
        sample_rate, audio_samples = wavfile.read(filename, 'rb')
        audio = AudioSegment.from_file(filename)
        temp_fname = f'temp_files/{time()}.wav'
        audio = audio.set_frame_rate(self.sample_rate).set_channels(1)
        audio.export(temp_fname, format = 'wav')
        sample_rate, audio_samples = wavfile.read(temp_fname, 'rb')
        audio_samples = audio_samples / float(self.MAX_ABS_INT16)
        return audio_samples

    def find_reference(self, funda):
        return [funda * ratio for ratio in self.reference_ratios]
    
    def output2hz(self, pitch_output):
        cqt_bin = pitch_output * self.PT_SLOPE + self.PT_OFFSET
        return self.FMIN * 2.0 ** (1.0 * cqt_bin / self.BINS_PER_OCTAVE)
    
    def fundamental_frequency(self, pitches):
        if pitches:
            return statistics.mean(heapq.nsmallest(10, pitches))
        else:
            return 0
    
    def run_model(self, audio_file):
        model_output = self.model.signatures["serving_default"](tf.constant(audio_file, tf.float32))
        pitch_outputs = model_output["pitch"]
        uncertainty_outputs = model_output["uncertainty"]
        confidence_outputs = list(1.0 - uncertainty_outputs)
        pitch_outputs = [float(n) for n in pitch_outputs]
        return pitch_outputs, confidence_outputs

    def pitch_window_to_notes(self, pitch_window, confidence_window, references):
        pitches = [
            elem[0] for elem in zip(pitch_window, confidence_window)
                if elem[1] > 0.9
        ]
        if pitches: # if some pitches are found with confidence more than 0.9
            freq = statistics.mean(pitches) # calculate their mean
            # identify the note whose frequency is closest to obtained frequency
            note_index = np.argmin([abs(reference - freq) for reference in references])
            return self.note_names[note_index] # return the corresponding note
        else: # else return none
            return None
        
    def transcript_pitch_to_notes(self, pitch, confidence, references, window_size):
        return [
            self.pitch_window_to_notes(
                pitch[num:num+window_size], 
                confidence[num:num+window_size], 
                references
            ) 
                for num in range(0, len(pitch), window_size)
        ]        
    
    def time_encodings(self, notes, window_size):
        interval = window_size * 0.032
        return [
            {
                "start_time": round(interval * ind, 3),
                "end_time": round(interval * (ind + 1), 3),
                "note": note
            }
                for ind, note in enumerate(notes)
        ]
    
    def note_transcription(self, file_name, window_size = 30):
        start = time()
        
        audio_file = self.load_audio_file(file_name)
        print("{:3f}".format(time() - start), "Loaded file")
        pitch, confidence = self.run_model(audio_file)
        pitch = list(map(self.output2hz, pitch))
        print("{:3f}".format(time() - start), "Model Prediction")
        base_freq = self.fundamental_frequency([el[0] for el in zip(pitch, confidence) if el[1] > 0.9])
        print("{:3f}".format(time() - start), "Base Frequency")
        references = self.find_reference(base_freq)
        print("{:3f}".format(time() - start), "References")
        notes = self.transcript_pitch_to_notes(pitch, confidence, references, window_size)
        print("{:3f}".format(time() - start), "Get Notes")
        time_encodings = self.time_encodings(notes, window_size)
        print("{:3f}".format(time() - start), "Time Encodings")
        return time_encodings


