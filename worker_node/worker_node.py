import sys
if len(sys.argv) > 0:
    server_url = sys.argv[1]
else:
    print("Please mention Server URL")
    exit() 

from flow_manager import flow_manager
from mongo_functions import *
from datetime import datetime
import traceback
flow_mgr = flow_manager()
database = my_db()
from time import sleep
import requests, json
os.makedirs('temp_files', exist_ok = True)
######################### imports end here

def process_main_video(data):
    # download audio
    database.update_process_status(data['_id'], 'processing')
    temp_audio = f"temp_files/{get_id()}.wav"
    database.read_audio(data['audio_id'], temp_audio)
    # create video
    # if data['process_type'] == 'base_audio':
    output_video, song_data = flow_mgr.make_tutorial(temp_audio)
    # else:
        # print(data.keys())
        # base_notes = database.uploaded_audios.find_one({'_id': data['base_id']})['song_data']['notes']
        # output_video, song_data = flow_mgr.make_tutorial(temp_audio, base_notes)
    video_id = database.write_video(output_video)
    os.remove(output_video)
    record = {
        'video_id': video_id,
        'video_type': 'main',
        'base_audio_id': data['audio_id'],
    }
    database.process_data.update_one(
        {'_id': data['_id']},
        {'$set': {'video_id': video_id}}
    )
    database.update_process_status(data['_id'], 'done')
    ua_record = {
        '_id': data['_id'],
        'user_id': data['user_id'],
        'video_id': video_id,
        'type': 'base',
        'song_data': song_data
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
        # exit()
