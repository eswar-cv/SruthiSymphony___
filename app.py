from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS, cross_origin
import datetime
import os, re
from queue import Queue
import requests
try:
    import yt_dlp as youtube_dl
except:
    os.system("""pip install https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz""")
    import yt_dlp as youtube_dl
# from flow_manager import flow_manager
from mongo_functions import *
from raga_identification import raga_identification
raga_identifier = raga_identification()
os.makedirs('yt_downloaded_files', exist_ok=True)
waits = {}
database = my_db('mongodb://localhost:27017')

print("Initializing flow manager")
# flow_mgr = flow_manager()

app = Flask(__name__)
CORS(app)

process_queue = Queue()
def yt_to_mp3(link, output_dir = 'yt_downloaded_files'):
    try:
        base_link = link[:]
        if len(link) == 11:
            link = f"https://www.youtube.com/watch?v={link}"
        else:
            base_link = link.split("/")[-1].split("=")[-1].replace("/", "_")
            if len(base_link) > 11:
                base_link = f'shorts_{base_link}'
        video_url = link
        video_info = youtube_dl.YoutubeDL().extract_info(url = video_url,download=False)
        filename = os.path.join(output_dir, f"{base_link}.mp3")
        options={
            'format':'bestaudio/best',
            'keepvideo':False,
            'outtmpl':filename,
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])

        print("Download Complete... {}".format(filename))
        return {'status': 'done', 'file': filename}
    except:
        print("Download Failed... {}".format(link))
        return {'status': 'failed', 'message': 'Something went wrong. Try with different link or Upload Audio.'}
# data will be stored in dictionary
# whenever some task comes it will be added to queue

os.makedirs("uploaded_files", exist_ok = True)
@app.route('/ping', methods=['POST', 'GET'])
def ping_pong():
    return "pong"

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return {"status": "failed"}

    file = request.files['audio']
    user_id = request.form.get('user_id')
    language = request.form.get('language')
    try:
        video_id = request.form.get('video_id')
        print('video_id', video_id)
    except:
        video_id = None
    try:
        start = request.form.get('start_point')
        print('start_point', start)
    except:
        start = None
    if not video_id:
        video_id = None
    if file:
        fpath = os.path.join('uploaded_files', file.filename)
        print(fpath)
        file.save(fpath)
        duration = AudioSegment.from_file(fpath).duration_seconds
        # date_and_time = str(datetime.datetime.now())
        # data to be added to queue
        process_id = get_id()
        audio_id = database.write_audio(fpath)
        # if video_id:
        #     song_data = database.uploaded_audios.find({'video_id': video_id})['song_data']
        queue_data = {
            "_id": process_id,
            "audio_id": audio_id,
            "process_type": "base_audio" if not video_id else "report",
            "user_id": user_id,
            "status": "in queue",
            "video": video_id,
            "duration": duration,
            'language': language,
            'start': start if start else 0
        }
        
        raga = raga_identifier.identify_raga(fpath)
        queue_data['raga'] = raga
        database.process_data.insert_one(queue_data) # adding data to db
        process_queue.put(queue_data)
        print(queue_data)
        return {"status": "done", "process_id": process_id} # in front-end UI keeps waiting for status



@app.route('/upload_youtube_url', methods=['POST'])
def upload_youtube_url():
    print("yt url")
    link = request.form.get("link")
    user_id = request.form.get('user_id')
    language = request.form.get('language')
    yt_download_response = yt_to_mp3(link)
    print(yt_download_response)
    video_id = None
    if yt_download_response['status'] == 'done':
        fpath = yt_download_response['file']
        duration = AudioSegment.from_file(fpath).duration_seconds
        # date_and_time = str(datetime.now())
        # data to be added to queue
        process_id = get_id()
        audio_id = database.write_audio(fpath)
        # if video_id:
        #     song_data = database.uploaded_audios.find({'video_id': video_id})['song_data']
        queue_data = {
            "_id": process_id,
            "audio_id": audio_id,
            "process_type": "base_audio" if not video_id else "report",
            "user_id": user_id,
            "status": "in queue",
            "video": video_id,
            'language': language
        }
        
        raga = raga_identifier.identify_raga(fpath)
        queue_data['raga'] = raga
        database.process_data.insert_one(queue_data) # adding data to db
        process_queue.put(queue_data)
        print(queue_data)
        return {"status": "done", "process_id": process_id} # in front-end UI keeps waiting for status



@app.route('/get_task', methods = ['POST'])
def get_task():
    return ""

@app.route('/get_video/<id>', methods = ['GET', 'POST'])
def get_video(id):
    if not id:
        return 'video not found', 404
    start, end = 0, None
    range_header = request.headers.get('Range', None)
    if range_header:
        range_match = re.search(r'bytes=(\d+)-(\d*)', range_header)
        start = int(range_match.group(1))
        end = range_match.group(2)
        end = int(end) if end else None
    file = f'temp_files/{id}.mp4'
    if not os.path.exists(file):
        database.read_video(id, file)
    size = os.path.getsize(file)
    if end:
        end = min(end, size - 1)
    else:
        end = size - 1
    
    length = end - start + 1
    
    with open(file, 'rb') as video:
        video.seek(start)
        data = video.read(length)

    response = Response(data, status=206, mimetype='video/mp4',
                        content_type='video/mp4', direct_passthrough=True)
    response.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, end, size))
    response.headers.add('Accept-Ranges', 'bytes')
    response.headers.add('Content-Length', str(length))
    
    return response

# @app.route('/get_video/<id>', methods = ['GET', 'POST'])
# def get_video(id):
#     start, end = 0, None
#     video = database.read_video(id)
#     if video:
#         return Response(video, mimetype = 'video/mp4')
#     else:
#         return 'video not found', 404

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def server1_proxy_1():
    # Forward the request to server 1 and return the response
    resp = requests.request(
        method=request.method,
        url=f"http://127.0.0.1:3000",
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    # Return the response content and status code
    return Response(resp.content, resp.status_code)

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def server1_proxy_2(path):
    # Forward the request to server 1 and return the response
    resp = requests.request(
        method=request.method,
        url=f"http://127.0.0.1:3000/{path}",
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    # Return the response content and status code
    return Response(resp.content, resp.status_code)

@app.route('/get_user_data/<id>', methods = ['GET', 'POST'])
def get_user_data(id):
    user_main = database.users.find_one({'_id': id})
    user_name = user_main['user']
    user_audios = database.uploaded_audios.find({'user_id': id}, {'_id': 1, 'user_id': 1, 'video_id': 1, 'type': 1})
    user_data = {
        'user': user_name,
        'id': id,
        'audios': list(user_audios)
    }
    return user_data

@app.route('/get_audio/<id>', methods = ['GET', 'POST'])
def get_audio(id):
#     audio = database.read_audio(id)
#     if audio:
#         return Response(audio, mimetype = 'audio/mp3')
#     else:
#         return 'audio not found', 404
    if not id:
        return 'video not found', 404
    start, end = 0, None
    range_header = request.headers.get('Range', None)
    if range_header:
        range_match = re.search(r'bytes=(\d+)-(\d*)', range_header)
        start = int(range_match.group(1))
        end = range_match.group(2)
        end = int(end) if end else None
    file = f'temp_files/{id}.wav'
    if not os.path.exists(file):
        database.read_video(id, file)
    size = os.path.getsize(file)
    if end:
        end = min(end, size - 1)
    else:
        end = size - 1
    
    length = end - start + 1
    
    with open(file, 'rb') as video:
        video.seek(start)
        data = video.read(length)

    response = Response(data, status=206, mimetype='audio/wav',
                        content_type='audio/wav', direct_passthrough=True)
    response.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, end, size))
    response.headers.add('Accept-Ranges', 'bytes')
    response.headers.add('Content-Length', str(length))
    
    return response

    # if data:
    #     print(data['link'])
    #     return "Acknowledgement: Data received"
    # else:
    #     return "No JSON data received"
@app.route('/validate_login', methods=['POST'])
def validate_login():
    data = request.get_json()
    result = database.validate_user(data['user'], data['password'])
    print('login', data, result)
    return result

@app.route('/get_queue_process', methods=['get'])
def get_queue_process():
    if len(process_queue.queue) > 0:
        temp_data = process_queue.get()
        print(temp_data)
        return temp_data
    else:
        print()
        return {'status': 'nothing_left'}

@app.route('/validate_signup', methods=['POST'])
def validate_signup():
    data = request.get_json()
    if data['user'] and data['password']:
        result = database.create_user(data['user'], data['password'])
        print('login', data, result)
        return result
    else:
        return {'status': 'failed', 'message': 'Please Enter Username and/or Password.'}

@app.route('/wait_status/<id>', methods = ['GET'])
def wait_status(id):
    match_in_queue = None
    counter = 0
    for record in process_queue.queue:
        counter += 1
        if record['_id'] == id:
            match_in_queue = record
            break
    if match_in_queue:
        return {'status': 'in queue', 'message': f'Waiting in Queue.\nPosition: {counter}'}
    db_status = database.get_process_data(id)
    # print(status)
    if db_status['status'] == 'done':
        print(db_status)
    return db_status

if __name__ == '__main__':
    app.run('0.0.0.0', port = 8000, threaded = True, debug=False)
