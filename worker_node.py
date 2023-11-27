from flow_manager import flow_manager
from mongo_functions import *
from datetime import datetime
from evaluation_note import evaluation_note
import traceback
try:
    lyrics_model
except:
    lyrics_model = 'small'
flow_mgr = flow_manager(lyrics_model)
try:
    mongo_uri
except:
    mongo_uri = 'mongodb://localhost:27017'
database = my_db(mongo_uri)
from time import sleep
try:
    server_url
except:
    server_url = 'http://localhost:8000'
import requests, json
os.makedirs('temp_files', exist_ok = True)
######################### imports end here

def process_main_video(data):
    # download audio
    database.update_process_status(data['_id'], 'processing')
    temp_audio = f"temp_files/{get_id()}.wav"
    database.read_audio(data['audio_id'], temp_audio)
    # create video
    print('process_type', data['process_type'])
    if data['process_type'] in ['base_audio', 'base_audios']:
        output_video, song_data = flow_mgr.make_tutorial(temp_audio, data['language'], data['raga'])
        base_audio_id = None
    else:
        print(data['process_type'])
        # print(data.keys())
        print('video_id', data['video'])
        print("Processing report audio")
        base_data_ = database.uploaded_audios.find_one({'video_id': data['video']})
        print(base_data_)
        print('LANGUAGE', base_data_['language'])
        temp_audio_2 = f"temp_files/{get_id()}.wav"
        dt = database.read_audio(base_data_['_id'], temp_audio_2)
        write_file = AudioSegment.from_file(temp_audio_2)[int(float(data['start']) * 1000):int(float(data['start'])+float(data['duration'])) * 1000]
        write_file.export(temp_audio_2, format = "wav")
        print("WRITEFILE WROTE", os.path.exists(temp_audio_2))
        base_data = flow_mgr.song_processing_agent.process_song(os.path.split(temp_audio_2)[-1], base_data_['language'])
        # note: user_note contains main note and note contains user_note
        output_video, song_data = flow_mgr.make_tutorial(temp_audio, base_data_['language'], data['raga'], base_data['notes'])
        
        base_audio_id = database.write_audio(temp_audio_2)
    video_id = database.write_video(output_video)
    os.remove(output_video)
    record = {
        'video_id': video_id,
        'video_type': 'main' if not base_audio_id else 'report',
        'base_audio_id': base_audio_id,
        
    }
    database.process_data.update_one(
        {'_id': data['_id']},
        {'$set': {'video_id': video_id, 'base_audio_id': base_audio_id}}
    )
    database.update_process_status(data['_id'], 'done')
    ua_record = {
        '_id': data['audio_id'],
        'user_id': data['user_id'],
        'video_id': video_id,
        'type': 'base' if data['process_type'] in ['base_audio', 'base_audios'] else 'report',
        'song_data': song_data,
        'language': data['language']
    }
    database.uploaded_audios.insert_one(ua_record)

def process_report_video(data):
    # download audio
    database.update_process_status(data['_id'], 'processing')
    temp_audio = f"temp_files/{get_id()}.wav"
    database.read_audio(data['audio_id'], temp_audio)
    # # create video
    # output_video, song_data = flow_mgr.make_tutorial(temp_audio)
    # video_id = database.write_video(output_video)
    # os.remove(output_video)
    # record = {
    #     'video_id': video_id,
    #     'video_type': 'main',
    #     'base_audio_id': data['audio_id'],
    # }
    # database.process_data.update_one(
    #     {'_id': data['_id']},
    #     {'$set': {'video_id': video_id}}
    # )
    # database.update_process_status(data['_id'], 'done')
    # ua_record = {
    #     '_id': data['_id'],
    #     'user_id': data['user_id'],
    #     'video_id': video_id,
    #     'type': 'base',
    #     'song_data': song_data
    # }
    # database.uploaded_audios.insert_one(ua_record)


######################### main process starts here
def get_process():
    response = requests.get(f'{server_url}/get_queue_process')
    data = json.loads(response.text)
    if data['status'] == 'nothing_left':
        print("All clear!")
        sleep(5)
    else: # new audio found
        print(data)
        process_main_video(data)

while True:
    print(datetime.now())
    try:
        get_process()
    except:
        print(traceback.print_exc())
        exit()
