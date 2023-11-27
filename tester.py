import requests

base_url = "http://localhost:6000"

def ping():
    url = f'{base_url}/ping'
    response = requests.post(url)
    if response.text == "pong":
        return True
    else:
        return False
    
def upload_file():
    url = f'{base_url}/upload_audio'
    files = {'file': open('output.wav', 'rb')}
    response = requests.post(url, files=files)
    print(response.text)  # Should print "File uploaded successfully"

upload_file()