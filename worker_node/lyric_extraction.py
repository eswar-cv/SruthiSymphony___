# %%
import os, subprocess, sys, json, shutil
from time import time
from ai4bharat.transliteration import XlitEngine

# %%
class lyric_extraction:
    def __init__(self):
        self.translation_engine = XlitEngine(src_script_type="indic", beam_width=10, rescore=False)
        print("Initialized multilingual model for translation")

    def make_command(self, track_path, output_dir, model, language):
        command = ['whisper', track_path, "--model", model, '--output_format', 'json', '--output_dir', output_dir]
        if language != "auto":
            command += ["--language", language]
        return command
    
    def transliterate(self, text, language):
        return self.translation_engine.translit_sentence(text, lang_code = "hi" if language == "auto" else language)

    def run_vocal_extraction(self, track_path, model = "medium", language = "auto"):
        temp_dir = os.path.join('temp_files', str(time()))
        file_name = os.path.splitext(os.path.split(track_path)[-1])[0]
        output_file = os.path.join(temp_dir, f'{file_name}.json')
        command = self.make_command(track_path, temp_dir, model, language)
        print(f"Running Lyric Extraction | Command: {' '.join(command)}")
        subprocess.run(command)
        if os.path.exists(output_file):
            whisper_output = json.load(open(output_file))
            lyrics = [
                {
                    "start_time": segment['start'],
                    "end_time": segment['end'],
                    "lyric": segment['text'] + " " + self.transliterate(segment['text'], language)
                }
                    for segment in whisper_output['segments']
            ]
        else:
            lyrics = []
        shutil.rmtree(temp_dir)
        return lyrics
        


