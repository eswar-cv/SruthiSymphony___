# %%
import os, subprocess, sys, json, shutil
from time import time
# from ai4bharat.transliteration import XlitEngine
import os
import whisper

# Disable GPU
# os.environ['CUDA_VISIBLE_DEVICES'] = ''

class lyric_extraction:
    def __init__(self, model_):
        self.model = whisper.load_model(model_)
    def run_vocal_extraction(self, track_path, language):
        print(f"Running Lyric Extraction [{language}]:", track_path)
        # res = whisper.transcribe(self.model, track_path)
        print(language)
        if language.strip().lower() != 'auto':
            res = self.model.transcribe(track_path, language = language, verbose = False)
        else:
            res = self.model.transcribe(track_path)
        lyrics = [
            {
                "start_time": segment['start'],
                "end_time": segment['end'],
                "lyric": segment['text']
            }
                for segment in res['segments']
        ]
        return lyrics

    
if __name__ == '__main__':
    lr = lyric_extraction('small')
    res = lr.run_vocal_extraction('test.mp3', language = 'Hindi')
    print(json.dumps(res, indent = 4))