# %%
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import demucs.separate
import subprocess
import numpy as np
from time import time
import shutil

# %%
class pre_processing:
    def __init__(self, sample_rate = 16000, input_dir = "raw_files", temp_dir = "temp_files", output_dir = "processed_files", save_format = "wav"):
        self.sample_rate = sample_rate
        self.input_dir = input_dir
        self.temp_dir = temp_dir
        self.output_dir = output_dir
        self.save_format = save_format
        os.makedirs(input_dir, exist_ok = True)
        os.makedirs(temp_dir, exist_ok = True)
        os.makedirs(output_dir, exist_ok = True)

    def demucs_command(self, files, input_dir = None, output_dir = None):
        # function to create demucs command for given input files
        if type(files) != list:
            if type(files) == np.ndarray:
                files = list(files)
            else:
                files = [files]
        # files = [f'{file}.mp3' for file in files] # removed as file type is not restricted to mp3
        if input_dir != None:
            files = [os.path.join(input_dir, file) for file in files]
        command = [f"--two-stems", "vocals"]
        if output_dir:
            command.append('-o')
            command.append(output_dir)
        return command, files

    def run_vocal_extraction(self, fnames, input_dir = None, output_dir = None):
        '''
        Runs vocal extraction of given files

        Given list of file names will process all files and saves to output directory
        '''
        command, files = self.demucs_command(fnames, input_dir, output_dir = output_dir)
        print("Running Command: " + " ".join(['demucs'] + command + files))
        try:
            demucs.separate.main(command + files)
        except:
            process = subprocess.Popen(['demucs'] + command + files, stdout = open("output.txt", "w"), stderr = open("error.txt", "w"))
            process.wait()
    
    def preprocess_files(self, fnames, input_dir = None, output_dir = None):
        if len(fnames) != len(set(fnames)):
            print("Files are not unique")
            return False
        if not input_dir: input_dir = self.input_dir
        if not output_dir: output_dir = self.output_dir
        temp_directory = os.path.join("temp_files", str(time()))
        # step 1: vocal extraction
        # running demucs command
        self.run_vocal_extraction(fnames, input_dir, temp_directory)
        separated_files = [
            (
                folder,
                os.path.join(temp_directory, 'htdemucs', folder, 'vocals.wav'),
                os.path.join(temp_directory, 'htdemucs', folder, 'no_vocals.wav'),
            )
                for folder in os.listdir(os.path.join(temp_directory, 'htdemucs'))
        ]
        store_outputs = []
        for file in separated_files:
            print(f"Running Stereo to Mono and Audio Resampling: {file}")
            fname, vocals, no_vocals = file
            vocals, no_vocals = AudioSegment.from_file(vocals), AudioSegment.from_file(no_vocals)
            # step 2: stereo to mono
            vocals, no_vocals = vocals.set_channels(1), no_vocals.set_channels(1)
            store_outputs.append(
                {
                    "vocals": os.path.join(output_dir, f'vocals.{fname}.{self.save_format}'), 
                    "no_vocals": os.path.join(output_dir, f'no_vocals.{fname}.{self.save_format}')
                }
            )
            # step 3: re-sample
            vocals, no_vocals = vocals.set_frame_rate(self.sample_rate), no_vocals.set_frame_rate(self.sample_rate)
            vocals.export(os.path.join(output_dir, f'vocals.{fname}.{self.save_format}'))
            no_vocals.export(os.path.join(output_dir, f'no_vocals.{fname}.{self.save_format}'))
        shutil.rmtree(temp_directory)
        print(store_outputs)
        return store_outputs
        

