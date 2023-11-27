# %%
import os, sys
from pre_processing import pre_processing
from note_identification import note_identification
from lyric_extraction import lyric_extraction
import subprocess
import soundfile as sf
# %%
class song_processor:
    def __init__(self):
        self.pre_processor = pre_processing(input_dir="temp_files")
        self.note_identifier = note_identification()
        self.lyric_extractor = lyric_extraction()

    def process_song(self, fname):
        pre_processed_files = self.pre_processor.preprocess_files([fname])[0]
        data, sample_rate = sf.read(pre_processed_files['vocals'])
        sf.write(pre_processed_files['vocals'], data, sample_rate)
        data, sample_rate = sf.read(pre_processed_files['no_vocals'])
        sf.write(pre_processed_files['no_vocals'], data, sample_rate)
        
        notes = self.note_identifier.note_transcription(pre_processed_files['vocals'])
        lyrics = []
        lyrics = self.lyric_extractor.run_vocal_extraction(pre_processed_files['vocals'])
        song_data = {
            "notes": notes,
            "lyrics": lyrics,
            "vocals": pre_processed_files['vocals'],
            "no_vocals": pre_processed_files['no_vocals']
        }
        return song_data





