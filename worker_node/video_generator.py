import json
import os
import tqdm
import cv2
from PIL import Image
import numpy as np
import os
import random
import tqdm
import librosa 
from image_maker import *
import soundfile as sf
import IPython.display as ipd
import numpy as np
import math
import shutil
import IPython.display as ipd
import cv2
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor
import copy
from moviepy.editor import ImageSequenceClip
from moviepy.editor import VideoFileClip, AudioFileClip, VideoClip
import datetime
from song_processor import song_processor
ll = ll = [['bhavapriyA', 'S1 R1 G2 M2 P D1 N2 S2', 'S2 N2 D1 P M2 G2 R1 S1'],
 ['cakravAkaM', 'S1 R1 G3 M1 P D2 N2 S2', 'S2 N2 D2 P M1 G3 R1 S1'],
 ['cala.NATTA', 'S1 R3 G3 M1 P D3 N3 S2', 'S2 N3 D3 P M1 G3 R3 S1'],
 ['cArukESi', 'S1 R2 G3 M1 P D1 N2 S2', 'S2 N2 D1 P M1 G3 R2 S1'],
 ['citrAMbari', 'S1 R2 G3 M2 P D3 N3 S2', 'S2 N3 D3 P M2 G3 R2 S1'],
 ['dharmavati', 'S1 R2 G2 M2 P D2 N3 S2', 'S2 N3 D2 P M2 G2 R2 S1'],
 ['dhAtuvardhani', 'S1 R3 G3 M2 P D1 N3 S2', 'S2 N3 D1 P M2 G3 R3 S1'],
 ['dhavalAmbari', 'S1 R1 G3 M2 P D1 N1 S2', 'S2 N1 D1 P M2 G3 R1 S1'],
 ['dhEnukA', 'S1 R1 G2 M1 P D1 N3 S2', 'S2 N3 D1 P M1 G2 R1 S1'],
 ['divyamaNi', 'S1 R1 G2 M2 P D3 N3 S2', 'S2 N3 D3 P M2 G2 R1 S1'],
 ['gamanaSrama', 'S1 R1 G3 M2 P D2 N3 S2', 'S2 N3 D2 P M2 G3 R1 S1'],
 ['gAnamUrti', 'S1 R1 G1 M1 P D1 N3 S2', 'S2 N3 D1 P M1 G1 R1 S1'],
 ['gAMgEyabhUshaNi', 'S1 R3 G3 M1 P D1 N3 S2', 'S2 N3 D1 P M1 G3 R3 S1'],
 ['gavAMbOdhi', 'S1 R1 G2 M2 P D1 N1 S2', 'S2 N1 D1 P M2 G2 R1 S1'],
 ['gAyakapriyA', 'S1 R1 G3 M1 P D1 N1 S2', 'S2 N1 D1 P M1 G3 R1 S1'],
 ['gaurimanOhari', 'S1 R2 G2 M1 P D2 N3 S2', 'S2 N3 D2 P M1 G2 R2 S1'],
 ['harikAMbhOji', 'S1 R2 G3 M1 P D2 N2 S2', 'S2 N2 D2 P M1 G3 R2 S1'],
 ['haTakAMbari', 'S1 R1 G3 M1 P D3 N3 S2', 'S2 N3 D3 P M1 G3 R1 S1'],
 ['hEmavati', 'S1 R2 G2 M2 P D2 N2 S2', 'S2 N2 D2 P M2 G2 R2 S1'],
 ['jalArNavaM', 'S1 R1 G1 M2 P D1 N2 S2', 'S2 N2 D1 P M2 G1 R1 S1'],
 ['jhAlavarALi', 'S1 R1 G1 M2 P D1 N3 S2', 'S2 N3 D1 P M2 G1 R1 S1'],
 ['jaMkAradhvani', 'S1 R2 G2 M1 P D1 N1 S2', 'S2 N1 D1 P M1 G2 R2 S1'],
 ['jyOtiSvarUpiNi', 'S1 R3 G3 M2 P D1 N2 S2', 'S2 N2 D1 P M2 G3 R3 S1'],
 ['kanakAMgi', 'S1 R1 G1 M1 P D1 N1 S2', 'S2 N1 D1 P M1 G1 R1 S1'],
 ['kAMtAmaNi', 'S1 R2 G3 M2 P D1 N1 S2', 'S2 N1 D1 P M2 G3 R2 S1'],
 ['kharaharapriyA', 'S1 R2 G2 M1 P D2 N2 S2', 'S2 N2 D2 P M1 G2 R2 S1'],
 ['kIravANi', 'S1 R2 G2 M1 P D1 N3 S2', 'S2 N3 D1 P M1 G2 R2 S1'],
 ['kOkilapriyA', 'S1 R1 G2 M1 P D2 N3 S2', 'S2 N3 D2 P M1 G2 R1 S1'],
 ['kOsalam', 'S1 R3 G3 M2 P D2 N3 S2', 'S2 N3 D2 P M2 G3 R3 S1'],
 ['latAMgi', 'S1 R2 G3 M2 P D1 N3 S2', 'S2 N3 D1 P M2 G3 R2 S1'],
 ['mAnavati', 'S1 R1 G1 M1 P D2 N3 S2', 'S2 N3 D2 P M1 G1 R1 S1'],
 ['mAraraMjani', 'S1 R2 G3 M1 P D1 N1 S2', 'S2 N1 D1 P M1 G3 R2 S1'],
 ['mAyAmALavagauLA', 'S1 R1 G3 M1 P D1 N3 S2', 'S2 N3 D1 P M1 G3 R1 S1'],
 ['mEcakalyANi', 'S1 R2 G3 M2 P D2 N3 S2', 'S2 N3 D2 P M2 G3 R2 S1'],
 ['nAgA.NaMdhini', 'S1 R2 G3 M1 P D3 N3 S2', 'S2 N3 D3 P M1 G3 R2 S1'],
 ['nAma.NArAyaNi', 'S1 R1 G3 M2 P D1 N2 S2', 'S2 N2 D1 P M2 G3 R1 S1'],
 ['nAsikAbhUshaNi', 'S1 R3 G3 M2 P D2 N2 S2', 'S2 N2 D2 P M2 G3 R3 S1'],
 ['naTabhairavi', 'S1 R2 G2 M1 P D1 N2 S2', 'S2 N2 D1 P M1 G2 R2 S1'],
 ['nATakapriyA', 'S1 R1 G2 M1 P D2 N2 S2', 'S2 N2 D2 P M1 G2 R1 S1'],
 ['navanItaM', 'S1 R1 G1 M2 P D2 N2 S2', 'S2 N2 D2 P M2 G1 R1 S1'],
 ['nItimati', 'S1 R2 G2 M2 P D3 N3 S2', 'S2 N3 D3 P M2 G2 R2 S1'],
 ['paMtuvarALi', 'S1 R1 G3 M2 P D1 N3 S2', 'S2 N3 D1 P M2 G3 R1 S1'],
 ['pAvani', 'S1 R1 G1 M2 P D2 N3 S2', 'S2 N3 D2 P M2 G1 R1 S1'],
 ['rAgavardhani', 'S1 R3 G3 M1 P D1 N2 S2', 'S2 N2 D1 P M1 G3 R3 S1'],
 ['raghupriyA', 'S1 R1 G1 M2 P D3 N3 S2', 'S2 N3 D3 P M2 G1 R1 S1'],
 ['ramapriyA', 'S1 R1 G3 M2 P D2 N2 S2', 'S2 N2 D2 P M2 G3 R1 S1'],
 ['rasikapriyA', 'S1 R3 G3 M2 P D3 N3 S2', 'S2 N3 D3 P M2 G3 R3 S1'],
 ['ratnAMgi', 'S1 R1 G1 M1 P D1 N2 S2', 'S2 N2 D1 P M1 G1 R1 S1'],
 ['rishabhapriyA', 'S1 R2 G3 M2 P D1 N2 S2', 'S2 N2 D1 P M2 G3 R2 S1'],
 ['rUpavati', 'S1 R1 G2 M1 P D3 N3 S2', 'S2 N3 D3 P M1 G2 R1 S1'],
 ['sAlagaM', 'S1 R1 G1 M2 P D1 N1 S2', 'S2 N1 D1 P M2 G1 R1 S1'],
 ['sarasAMgi', 'S1 R2 G3 M1 P D1 N3 S2', 'S2 N3 D1 P M1 G3 R2 S1'],
 ['sEnAvati', 'S1 R1 G2 M1 P D1 N1 S2', 'S2 N1 D1 P M1 G2 R1 S1'],
 ['shaDvitamArgiNi', 'S1 R1 G2 M2 P D2 N2 S2', 'S2 N2 D2 P M2 G2 R1 S1'],
 ['shaNmukhapriyA', 'S1 R2 G2 M2 P D1 N2 S2', 'S2 N2 D1 P M2 G2 R2 S1'],
 ['sUlini', 'S1 R3 G3 M1 P D2 N3 S2', 'S2 N3 D2 P M1 G3 R3 S1'],
 ['SyAmaLAMgi', 'S1 R2 G2 M2 P D1 N1 S2', 'S2 N1 D1 P M2 G2 R2 S1'],
 ['siMhEMdramadhyamam', 'S1 R2 G2 M2 P D1 N3 S2', 'S2 N3 D1 P M2 G2 R2 S1'],
 ['SubhapaMtuvarALi', 'S1 R1 G2 M2 P D1 N3 S2', 'S2 N3 D1 P M2 G2 R1 S1'],
 ['sucaritrA', 'S1 R3 G3 M2 P D1 N1 S2', 'S2 N1 D1 P M2 G3 R3 S1'],
 ['sUryakAMtaM', 'S1 R1 G3 M1 P D2 N3 S2', 'S2 N3 D2 P M1 G3 R1 S1'],
 ['suvarNAMgi', 'S1 R1 G2 M2 P D2 N3 S2', 'S2 N3 D2 P M2 G2 R1 S1'],
 ['tAnarUpi', 'S1 R1 G1 M1 P D3 N3 S2', 'S2 N3 D3 P M1 G1 R1 S1'],
 ['vAcaspati', 'S1 R2 G3 M2 P D2 N2 S2', 'S2 N2 D2 P M2 G3 R2 S1'],
 ['vAgadhISvari', 'S1 R3 G3 M1 P D2 N2 S2', 'S2 N2 D2 P M1 G3 R3 S1'],
 ['vakuLAbharaNam', 'S1 R1 G3 M1 P D1 N2 S2', 'S2 N2 D1 P M1 G3 R1 S1'],
 ['vanaspati', 'S1 R1 G1 M1 P D2 N2 S2', 'S2 N2 D2 P M1 G1 R1 S1'],
 ['varuNapriyA', 'S1 R2 G2 M1 P D3 N3 S2', 'S2 N3 D3 P M1 G2 R2 S1'],
 ['viSvAmbhari', 'S1 R1 G3 M2 P D3 N3 S2', 'S2 N3 D3 P M2 G3 R1 S1'],
 ['yAgapriyA', 'S1 R3 G3 M1 P D1 N1 S2', 'S2 N1 D1 P M1 G3 R3 S1']]
class video_generator:
    def __init__(self, default_padding = 0.5, length = 800, default_border_radius = 20):
        self.default_padding = default_padding
        self.length = length
        self.size = (length, length)
        self.default_border_radius = default_border_radius

        # self.color_1 = (148, 119, 62)
        # self.color_2 = (219, 158, 73)
        # self.color_3 = (186, 110, 17)
        # self.color_4 = (40, 59, 62)
        # self.color_5 = (201, 112, 10)
        # self.color_6 = (54, 72, 76)
        # self.color_7 = tuple(int(color * 1.1) for color in self.color_2)

        self.color_1 = self.hex_to_rgb("#EEE2DC") # border
        self.color_2 = self.hex_to_rgb("#AC3B61") # part
        self.color_3 = self.hex_to_rgb("#EDC7B7") # background
        self.color_4 = self.hex_to_rgb("#123456") # title, progress status
        self.color_5 = self.hex_to_rgb("#123C69") # part
        self.color_6 = self.hex_to_rgb("#327ac2") # progress bar
        self.color_7 = tuple(int(color * 1.1) for color in self.color_2)

    def hex_to_rgb(self, hex_code):
        hex_code = hex_code.lstrip('#')
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)
        return (r, g, b)
    
    def get_val(self, percent, length = None):
        if length == None:
            length = self.length
        return int((percent / 100) * length)

    def get_box_dims(self, x_start, y_start, x_end, y_end, padding = 25, mapper_function = None):
        if mapper_function == None:
            mapper_function = self.get_val
        if type(padding) in [int, float]:
            padding = (padding, padding, padding, padding)
        elif len(padding) == 2:
            padding = (padding[0], padding[1], padding[0], padding[1])
        x_start, y_start, x_end, y_end = map(mapper_function, [x_start, y_start, x_end, y_end]) # following sequence from CSS padding format
        return ((x_start + padding[3], y_start + padding[0]), (x_end - padding[1], y_end - padding[2]))

    def draw_box(self, draw, xp_start, xp_end, yp_start, yp_end, color, padding = None, border_radius = None):
        if padding == None: padding = self.default_padding
        if border_radius == None: border_radius = self.default_border_radius
        box_dims = self.get_box_dims(xp_start, yp_start, xp_end, yp_end, padding)
        draw.rounded_rectangle(box_dims, border_radius, color)
    
    def create_base_image(self, mode = "RGB", size = None, TrackId = 123456789, TrackName = 'abcd',UserName = "NA", Accuracy = 'helloworldhello', RagaName = "SampleRagaName", RagaNumber = 30, Arohanam = "A B C D E F", Avarohanam = "F E D C B A", total = 100):
        if not size: size = self.size
        if len(UserName) > 14:
            UserName = UserName[0:6] + '..' + UserName[-6:]
        if len(TrackName) > 32:
            TrackName = TrackName[0:15] + '..' + TrackName[-15:]
        img = Image.new("RGBA", size, (0,0,0,0))
        draw = ImageDraw.Draw(img, 'RGBA')
        # img = Image.open("sample.jpg").convert("RGB")
        size_x, size_y = size
        # under ############################################################
        self.draw_box(draw, 0, 100, 0, 100, self.color_1, border_radius = 0)
        # main #############################################################
        self.draw_box(draw, 0, 100, 0, 100, self.color_2, padding = 10)
        # box 0 - App Title ################################################
        ## main box
        self.draw_box(draw, 0, 100, 0, 10, self.color_3, padding = (20, 20, 5, 20))
        ## Text - App Title
        TextInsert(img, "Sruthi Symphony: Carnatic Music Tutorial App", X = 50, Y = 5.575, TextColor = self.color_4, FontSize=0.0266 * size_y, stroke = 0.5)
        # box 1 - track details ############################################
        ## main box
        self.draw_box(draw, 0, 100, 10, 20, self.color_3, padding = (5, 20))
        ### Track Id
        self.draw_box(draw, 0, 25, 10, 20, self.color_5, padding = (20, 10, 20, 35))
        TextInsert(img, f"Id: {TrackId}", X = 25/2 + (10/size_x) * 100, Y = 14.75, TextColor = self.color_6, FontSize=0.02 * size_y)
        ### Track Name
        self.draw_box(draw, 25, 75, 10, 20, self.color_5, padding = (20, 10, 20, 10))
        TextInsert(img, TrackName, X = 50, Y = 14.75, TextColor = self.color_6, FontSize=0.02 * size_y, stroke=0.45)
        ### Track User 
        self.draw_box(draw, 75, 100, 10, 20, self.color_5, padding = (20, 35, 20, 10))
        TextInsert(img, f"By: {UserName}", X = 75 + 25/2 - (10/size_x) * 100, Y = 14.75, TextColor = self.color_6, FontSize=0.02 * size_y)
        # box 2 - raga #####################################################
        ## main box
        self.draw_box(draw, 0, 100, 20, 40, self.color_3, padding = (5, 20))
        ### Raga Number and Name
        self.draw_box(draw, 0, 40, 20, 40, self.color_5, padding = (20, 10, 20, 35))
        TextInsert(img, f"Raga {RagaNumber}", X = 20 + (10/size_x) * 100, Y = 26.75, TextColor = self.color_6, FontSize=0.02 * size_y)
        TextInsert(img, f"{RagaName} Raga", X = 20 + (10/size_x) * 100, Y = 32.75, TextColor = self.color_6, FontSize=0.02 * size_y)
        ### Raga Arohanam
        self.draw_box(draw, 40, 100, 20, 30, self.color_5, padding = (20, 35, 10, 10))
        TextInsert(img, "Arohanam:", X = 50 + (10/size_x) * 100, Y = 24.75, TextColor = self.color_6, FontSize=0.02 * size_y)
        TextInsert(img, Arohanam, X = 80 + (10/size_x) * 100, Y = 24.75, TextColor = self.color_6, FontSize=0.02 * size_y)
        ### Raga Avarohanam
        self.draw_box(draw, 40, 100, 30, 40, self.color_5, padding = (10, 35, 20, 10))
        TextInsert(img, "Avarohanam:", X = 50 + (10/size_x) * 100, Y = 34.75, TextColor = self.color_6, FontSize=0.02 * size_y)
        TextInsert(img, Avarohanam, X = 80 + (10/size_x) * 100, Y = 34.75, TextColor = self.color_6, FontSize=0.02 * size_y)
        # box 3 - note #####################################################
        ## main box
        self.draw_box(draw, 0, 100, 40, 70, self.color_3, padding = (5, 20))
        
        # box 4 - progress #################################################
        ## main box
        self.draw_box(draw, 0, 100, 70, 80, self.color_3, padding = (5, 20))
        self.draw_box(draw, 1, 99, 71, 79, self.color_5, padding = (5, 20))
        # move this to new function    
        # img = ProgressBar(img, X = 50, Y = 50, width = (0.8 * size_x), height = (0.2 * 0.4 * size_y), innercolor=color_5)
        # box 5 - lyrics ###################################################
        ## main box
        self.draw_box(draw, 0, 100, 80, 100, self.color_3, padding = (5, 20, 20, 20))

        return img
    
    def create_frame_image(self, image, lyrics = None, note = None, user_note = None, total = 100, current = 0):
        start = time()
        size_x, size_y = self.size
        img = copy.deepcopy(image)
        draw = ImageDraw.Draw(img, 'RGBA')
        # progress
        progress = (current/total) * 100
        if progress < 8:
            progress = 8
        self.draw_box(draw, 1, progress - 1, 71, 79, self.color_4, padding = (5, 20))
        TextInsert(img, f"{datetime.timedelta(seconds=int(current))}/{datetime.timedelta(seconds=total)}", X = 50, Y = 75, TextColor = self.color_7, FontSize=0.0266 * size_y, stroke = 0.5)
        # lyrics
        llen = len(lyrics)
        lyrics = lyrics.split()    
        
        if llen > 40:
            lyrics_wordlen = len(lyrics)
            split_zone = lyrics_wordlen // 2 + (1 if lyrics_wordlen % 2 == 1 else 0)
            line1, line2 = lyrics[0:split_zone], lyrics[split_zone:]
        else:
            line1, line2 = lyrics, []
        
        if line2:
            TextInsert(img, " ".join(line1), X = 50, Y = 86, TextColor = self.color_6, FontSize=0.03 * size_y, shrink=False)
            TextInsert(img, " ".join(line2), X = 50, Y = 93, TextColor = self.color_6, FontSize=0.03 * size_y, shrink=False)
        else:
            TextInsert(img, " ".join(line1), X = 50, Y = 89, TextColor = self.color_6, FontSize=0.03 * size_y, shrink=False)
        
        TextInsert(img, note, X = 50, Y = 50, TextColor=self.color_6, FontSize=0.045 * size_y)
        TextInsert(img, user_note, X = 50, Y = 58, TextColor=self.color_6 if note == user_note else (240, 30, 30), FontSize=0.045 * size_y)
        
        return img

    # image = create_new_image(TrackName='abcd' * 60, current=257, total=500)
    # image.save("temp.png")
    # image
    def map_data_with_frame(self, lyrics, duration, fps):
        total_frames = int(duration * fps)
        print('total frames', total_frames)
        lyric_mappings = [None for _ in range(total_frames)]
        for ind, lyric in enumerate(lyrics):
            start_frame, end_frame = int(lyric['start_time'] * fps), int(lyric['end_time'] * fps)
            # print(ind, start_frame, end_frame)
            for idx in range(start_frame, end_frame + 1):
                try:
                    lyric_mappings[idx] = ind
                except:
                    print('ERROR', ind)
        return lyric_mappings
    
    def pass_dict_to_frame_maker(self, dictionary):
        return self.create_frame_image(**dictionary)


    def to_cv2_req_format(self, im):
        return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    
    def make_demo_video(self, track_name, song_data, duration, fps = 10):
        lyrics = song_data['lyrics']
        notes = song_data['notes']
        user_notes = song_data['user_notes']
        lyric_mappings = self.map_data_with_frame(song_data['lyrics'], duration, fps)
        note_mappings = self.map_data_with_frame(song_data['notes'], duration, fps)
        user_note_mappings = self.map_data_with_frame(song_data['user_notes'], duration, fps)
        print(len(lyric_mappings))
        print(len(note_mappings))
        try:
            raga = ll[int(1200//duration)]
        except:
            raga = ll[4]
        song_data = {
            "TrackId": "NA",
            "TrackName": "Uploaded Audio",
            "Accuracy": song_data['accuracy'] if 'accuracy' in song_data else 'None',
            "RagaName": raga[0],
            "Arohanam": raga[1],
            "Avarohanam": raga[2],
            "total": duration
        }
        base_image = self.create_base_image(**song_data)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_fname = f"video_output_" + str(time()).split('.')[0] + '.mp4'
        video_writer = cv2.VideoWriter(os.path.join("", video_fname), fourcc, fps, self.size)
        current_multiply_factor = (1/fps)
        all_data = [
            {
                'image': base_image,
                'lyrics': str(lyrics[lyric_mappings[ind]]['lyric']) if lyric_mappings[ind] != None else "", 
                'note': str(notes[note_mappings[ind]]['note']) if note_mappings[ind] != None else "", 
                'user_note': str(user_notes[user_note_mappings[ind]]['note']) if user_note_mappings[ind] != None else "", 
                'total': duration,
                'current': current_multiply_factor * ind
            }
            for ind, _ in enumerate(note_mappings)
        ]
        for frame in tqdm.tqdm(map(self.pass_dict_to_frame_maker, all_data), total = len(all_data)):
            video_writer.write(self.to_cv2_req_format(frame))
        # for ind, mapping in enumerate(lyric_mappings):
        #     data = {
        #         'image': base_image,
        #         'lyrics': lyrics[mapping]['lyric'] if mapping else "", 
        #         'total': duration,
        #         'current': int(current_multiply_factor * ind) + 1
        #         }
        #     temp_image = create_frame_image(**data)
        #     video_writer.write(to_cv2_req_format(temp_image))
        video_writer.release()
        os.system(f"ffmpeg -i {video_fname} -i {track_name} output_{video_fname}")
        return f"output_{video_fname}"
    