import os
from pydub import AudioSegment
from time import time
import soundfile as sf
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.utils import load_img, img_to_array
from PIL import Image
import tqdm
import json
import tensorflow as tf
from collections import Counter
tf.config.set_visible_devices([], 'GPU')
class raga_identification:
    def __init__(self, model = 'raga_model.h5'):
        self.model = tf.keras.models.load_model(model)
        self.class_indices = {'1': 0, '10': 1, '11': 2, '12': 3, '13': 4, '14': 5, '15': 6, '16': 7, '17': 8, '18': 9, '19': 10, '2': 11, '20': 12, '21': 13, '22': 14, '23': 15, '24': 16, '25': 17, '26': 18, '27': 19, '28': 20, '29': 21, '3': 22, '30': 23, '31': 24, '32': 25, '33': 26, '34': 27, '35': 28, '36': 29, '37': 30, '38': 31, '39': 32, '4': 33, '40': 34, '41': 35, '42': 36, '43': 37, '44': 38, '45': 39, '46': 40, '47': 41, '48': 42, '49': 43, '5': 44, '50': 45, '51': 46, '52': 47, '53': 48, '54': 49, '55': 50, '56': 51, '57': 52, '58': 53, '59': 54, '6': 55, '60': 56, '61': 57, '62': 58, '63': 59, '64': 60, '65': 61, '66': 62, '67': 63, '68': 64, '69': 65, '7': 66, '70': 67, '71': 68, '72': 69, '8': 70, '9': 71}
        self.raga_names = {'20': ['Bhairavi', 'Natabhairavi'], '44': ['Bhavapriya'], '16': ['Chakravakam'], '36': ['Chalanata'], '26': ['Charukesi'], '66': ['Chithrambari'], '59': ['Dharmavathi'], '69': ['Dhatuvardhani'], '49': ['Dhavalambari'], '9': ['Dhenuka'], '48': ['Dhivyamani'], '53': ['Gamanashrama'], '3': ['Ganamoorthi'], '33': ['Gangeyabhushani'], '43': ['Gavambodhi'], '13': ['Gayakapriya'], '15': ['Gowla', 'Mayamalavagowla'], '23': ['Gowrimanohari'], '28': ['Harikambhoji', 'Kambhoji'], '18': ['Hatakambari'], '58': ['Hemavathi'], '38': ['Jalarnavam'], '39': ['Jalavarali', 'Varali'], '19': ['Jankaradhvani'], '68': ['Jyothi', 'Jyothiswaroopini'], '65': ['Kalyani', 'Mechakalyani'], '1': ['Kanakangi'], '61': ['Kanthamani'], '22': ['Karaharapriya'], '21': ['Keeravani'], '11': ['Kokilapriya'], '71': ['Kosalam'], '63': ['Lathangi'], '5': ['Manavathi'], '25': ['Mararanjani'], '30': ['Naganandhini'], '50': ['Namanarayani'], '70': ['Nasikabhushani'], '10': ['Natakapriya'], '40': ['Navanitham'], '60': ['Neethimathi'], '51': ['Panthuvarali'], '41': ['Pavani'], '32': ['Ragavardhani'], '42': ['Raghupriya'], '52': ['Ramapriya'], '72': ['Rasikapriya'], '2': ['Rathnangi'], '62': ['Rishabhapriya'], '12': ['Rupavathi'], '37': ['Salagam'], '29': ['Sankarabharanam'], '27': ['Sarasangi'], '7': ['Senavathi'], '46': ['Shadhvidhamargini'], '56': ['Shanmukapriya'], '35': ['Shulini'], '55': ['Shyamalangi'], '57': ['Simhendramadhyamam'], '45': ['Subhapanthuvarali'], '67': ['Sucharithra'], '17': ['Suryakantam'], '47': ['Suvarnangi'], '6': ['Thanarupi'], '8': ['Thodi'], '64': ['Vachaspathi'], '34': ['Vagadheeswari'], '14': ['Vakulabharanam'], '4': ['Vanaspathi'], '24': ['Varunapriya'], '54': ['Vishwambhari'], '31': ['Yagapriya']}
        self.class_from_argmax = {self.class_indices[key]: key for key in self.class_indices}
        os.makedirs('temp_files', exist_ok=True)

    def make_images_for_song(self, song_path, duration = 30): # vocals audio as input
        audio = AudioSegment.from_file(song_path)
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        temp_dir = os.path.join('temp_files', str(time())) # used to store images
        os.makedirs(temp_dir, exist_ok=True)
        chunks = [audio[ind * 1000 : (ind + duration) * 1000] for ind in range(0, int(audio.duration_seconds // 30 + 1))]
        temp_audio = os.path.join('temp_files', str(time()) + '.wav')
        paths = []
        for ind, chunk in enumerate(tqdm.tqdm(chunks, desc = '[Raga] Generating Images')):
            if chunk.duration_seconds >= 29:
                chunk.export(temp_audio, format = 'wav')
                audio, sr = sf.read(temp_audio)
                sf.write(temp_audio, audio, sr)
                data, sample_rate = librosa.load(temp_audio)
                # Calculate the spectrogram
                window_size = 1024
                hop_length = int(window_size / 2)
                spectrogram = librosa.amplitude_to_db(np.abs(librosa.stft(data, n_fft=window_size, hop_length=hop_length)))
                # Plot the spectrogram in grayscale
                plt.figure(figsize=(8, 8))
                plt.imshow(spectrogram, origin='lower', aspect='auto')
                plt.axis('off')
                fname = os.path.split(temp_audio)[-1]
                main_name, extension = os.path.splitext(fname)
                save_path = os.path.join('temp_files', f'{main_name}_{ind}.jpg')
                plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
                plt.close()
                paths.append(save_path)
        return paths
    
    def predict_image(self, image_path, target_size = 256):
        test_image=load_img(image_path,target_size=(target_size, target_size))
        test_image=img_to_array(test_image)
        test_image=test_image/255
        test_image=np.expand_dims(test_image,axis=0)
        result=self.model.predict(test_image)
        result=np.argmax(result)
        return result
    
    def identify_raga(self, audio_path):
        print(audio_path)
        images = self.make_images_for_song(audio_path)
        print('all images', len(images))
        predictions = [self.predict_image(image) for image in tqdm.tqdm(images, desc = '[Raga] Predicting')]
        counts = {}
        for pred in predictions:
            if pred in counts:
                counts[pred] += 1
            else:
                counts[pred] = 1
        pred_counts = [(item, count) for item, count in counts.items()]
        print(counts)
        print(pred_counts)
        pred_counts.sort(key = lambda x: x[1], reverse = True)
        try:
            max_element = pred_counts[0][0]
            raga_data = json.load(open(f'raga_metadata/{self.raga_names[self.class_from_argmax[max_element]][0]}.json'))
            arohanam, avarohanam = raga_data['info'][1]['V'][1], raga_data['info'][2]['V'][1]
            return {
                'raga_number': self.class_from_argmax[max_element],
                'raga_name': self.raga_names[self.class_from_argmax[max_element]][0],
                'arohanam': arohanam,
                'avarohanam': avarohanam
            }
        except:
            return {
                'raga_number': 'NA',
                'raga_name': 'NA',
                'arohanam': 'NA',
                'avarohanam': 'NA',
            }
