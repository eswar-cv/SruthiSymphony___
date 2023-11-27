import os
import tqdm
try:
    import yt_dlp as youtube_dl
except:
    os.system("""pip install https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz""")
    import yt_dlp as youtube_dl
import json
import copy
from time import time
os.makedirs('yt_downloaded_files', exist_ok=True)

def yt_to_mp3(link, audio_id, output_dir = 'uploaded_files'):
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
        filename = os.path.join(output_dir, f"{audio_id}.mp3")
        options={
            'format':'bestaudio/best',
            'keepvideo':False,
            'outtmpl':filename,
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])

        print("Download Complete... {}".format(filename))
        return filename
    except:
        print("Download Failed... {}".format(link))
        return False
    
def get_id():
    return str(time().strip(".")[0])
