# %%

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from gridfs import GridFS
from time import time
from pydub import AudioSegment
import os
import soundfile as sf
from datetime import datetime
# %%
def get_id():
    return str(datetime.now()).replace(':', '_').replace(' ', '_').replace('-', '_') # id is timestamp. 

# %%
class my_db:
    def __init__(self, mongo_uri, user = "admin", password = "FxTrZgPAQCRnMXer"):
        self.db = MongoClient(mongo_uri)['Capstone']
        self.files = self.db['files'] # files storage
        self.users = self.db['users'] # user credentials
        self.uploaded_audios = self.db['uploaded_audios']
        self.process_data = self.db['process_data'] # processing stage of songs will be mentioned here
        os.makedirs('temp_files', exist_ok = True)
    
    def create_user(self, user, password):
        # check if user already exists
        users = self.users.find({'user': user})
        if len(list(users)) > 0:
            return {"status": "failed", "message": f"User '{user}' Already Exists"}
        else:
            user_id = get_id()
            user_record = {
                "user": user,
                "password": password,
                "_id": user_id
            }
            self.users.insert_one(user_record) # insert user's credentials
            return {"status": "done", "message": f"New User '{user}' Created."}
        
    def validate_user(self, user, password):
        matched_users = list(self.users.find({'user': user}))
        if matched_users:
            if matched_users[0]['password'] == password:
                return {'status': 'done', 'id': matched_users[0]['_id'], 'message': 'User Logged In.'}
            else:
                return {'status': 'failed', 'message': 'Invalid Password.'}
        else:
            return {'status': 'failed', 'message': 'Invalid User.'}
        
    def write_audio(self, file_path):
        # read audio using PyDub
        audio_file = AudioSegment.from_file(file_path)
        audio_file = audio_file.set_channels(1)
        id = get_id()
        temp_file = f'temp_files/{id}.mp3'
        audio_file.export(temp_file, format = "mp3")
        file = open(temp_file, 'rb')
        file_contents = file.read()
        file.close()
        record = {
            "_id": id,
            "content": file_contents
        }
        self.files.insert_one(record)
        return id

    def read_audio(self, id, file_path = None):
        records = list(self.files.find({"_id": id}))
        temp_id = get_id()
        if records:
            if file_path:
                with open(f'temp_files/{temp_id}.mp3', 'wb') as file:
                    file.write(records[0]['content'])
                audio = AudioSegment.from_file(f'temp_files/{temp_id}.mp3')
                audio.export(f'temp_files/{temp_id}.wav', format = "wav")
                wav_data, sample_rate = sf.read(f'temp_files/{temp_id}.wav')
                sf.write(file_path, wav_data, sample_rate)
            return records[0]['content']
        else:
            return print("FAILED TO FETCH FILE")

    def write_video(self, file_path):
        # generate id
        id = get_id()
        file = open(file_path, 'rb')
        file_contents = file.read()
        file.close()
        record = {
            "_id": id,
            "content": file_contents,
        }
        self.files.insert_one(record)
        return id
    
    def read_video(self, id, file_path = None):
        id = str(id)
        records = list(self.files.find({"_id": id}))
        if records:
            if file_path:
                with open(file_path, 'wb') as file:
                    file.write(records[0]['content'])
            return records[0]['content']
        else:
            return False
    
    def add_song_to_user(self, user_id, category, data):
        '''category => `base_audios` or `recorded_audios`'''
        self.user_data.update_one(
            {'_id': user_id},
            {'$push': {category: data}}
            )
        
    def add_video_to_user(self, user_id, category, data):
        '''category => `base_audios` or `recorded_audios`'''
        self.user_data.update_one(
            {'_id': user_id},
            {'$push': {category: data}}
            )
    
    def update_process_status(self, process_id, status):
        self.process_data.update_one(
            {'_id': process_id},
            {'$set': {'status': status}}
        )

    def get_process_data(self, id):
        record = list(self.process_data.find({'_id': id}))
        if record:
            record = record[0]
            return {'status': record['status'], 'message': record['status'], 'video_id': record['video_id'] if 'video_id' in record else None, 'base_audio_id': record['base_audio_id'] if 'base_audio_id' in record else None, 'accuracy': record['accuracy'] if 'accuracy' in record else None}
        else:
            return {'status': 'failed', 'message': 'Process not found. Try checking home page or sing/upload the audio again.'}

    def store_uploaded_song(self, file_path, user_id):
        # store the file in DB and get id
        id = self.write_audio(file_path)
        fname = os.path.split(file_path)[-1]
        name = os.path.splitext(fname)[0]
        duration = AudioSegment.from_file(file_path).duration_seconds


if __name__ == "__main__":
    database = my_db()
    print(list(database.user_data.find()))
    print(list(database.process_data.find()))
    # print(list(database.user_data.find()))