import React, { createRef, useState, useRef, fileInput } from 'react';
export default class UploadAudio extends React.Component {
    // props - url
    constructor(props) {
        super(props);
        this.state = {"upload_type": "File"} // upload method - File or YouTube
        
        this.HandleYoutubeLink = this.HandleYoutubeLink.bind(this);
        this.HandleAudio = this.HandleAudio.bind(this);
        this.getYouTubeVideoId = this.getYouTubeVideoId.bind(this);
        this.manage_url_change = this.manage_url_change.bind(this);
        this.componentDidMount = this.componentDidMount.bind(this);
        this.YT_UI = this.YT_UI.bind(this);
        this.AU_UI = this.AU_UI.bind(this);
        this.auref = createRef();
        this.ytref = createRef();
    }

    YT_UI(event) {
        console.log(event.target);
        this.setState({"upload_type": "YouTube"});
        this.setState({"upload_ui": <YoutubeUploadUI callback = {this.HandleYoutubeLink}/>});
    }

    AU_UI(event) {
        console.log(event.target);
        this.setState({"upload_type": "File"});
        this.setState({"upload_ui": <AudioPlayer callback = {this.HandleAudio}/>});
    }



    componentDidMount() {
        console.log("Mounted");
        if (this.state.upload_type == "YouTube") {
            this.setState({"upload_ui": <YoutubeUploadUI callback = {this.HandleYoutubeLink}/>});
        }
        else {
            this.setState({"upload_ui": <AudioPlayer callback = {this.HandleAudio}/>});
        }
    }

    manage_url_change() {

    }
    HandleYoutubeLink(link) {
        // alert("Submitted YouTube Video: " + link);
        const form_data = new FormData();
            form_data.append("link", link);
            form_data.append("user_id", localStorage.getItem('capstone_user_id'));
            form_data.append("language", document.querySelector('select').value);
            
            fetch(`${this.props.server_url}/upload_youtube_url`, {
                method: 'POST',
                body: form_data
            }).then(response => {
                if (response.ok) { // response is okay
                    const data = response.json();
                    data.then(
                        res=> {
                            if (res['status'] == 'done') {
                                // alert('Audio uploaded. Id: ' + res['process_id']);
                                window.location.assign(`/wait?id=${res['process_id']}`);
                            }
                            else {
                                alert("Something Went Wrong. Please try again.");
                            }
                        }
                    )
                }
                else {
                alert('Upload failed.');
                }
            }).catch(error => {
                console.error('Error: ' + error);
            });
    }

    HandleAudio(file) {
        if (file) {
            console.log(file['name']);
            const form_data = new FormData();
            form_data.append("audio", file, "base_song.wav");
            form_data.append("user_id", localStorage.getItem('capstone_user_id'));
            form_data.append("language", document.querySelector('select').value);
            fetch(`${this.props.server_url}/upload_audio`, {
                method: 'POST',
                body: form_data
            }).then(response => {
                if (response.ok) { // response is okay
                    const data = response.json();
                    data.then(
                        res=> {
                            console.log("upload response " + res);
                            console.log(res['status'])
                            if (res['status'] == 'done') {
                                window.location.assign(`/wait?id=${res['process_id']}`);
                            }
                        }
                    )
                }
                else {
                alert('Upload failed.');
                }
            }).catch(error => {
                console.error('Error: ' + error);
            });
            
        }
        else {
            alert("Upload a file.")
        }
        
    }

    getYouTubeVideoId(link) {
        const patterns = [
          /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/shorts\/)([A-Za-z0-9_-]+)/,
          /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/shorts\/)([A-Za-z0-9_-]+)&/,
        ];
        for (const pattern of patterns) {
          const match = link.match(pattern);
          if (match) {
            return match[1];
          }
        }
        return null;
    }

    render() {
        return (
            <div id = "UploadAudio" className = "fill">
                <div id = "UploadMethod" className = "fill">
                    <div ref = {this.auref}><button onClick = {this.AU_UI}>File</button></div>
                    <div ref = {this.ytref}><button onClick = {this.YT_UI}>Youtube</button></div>                    
                </div>
                {this.state.upload_ui}
                <div id = "select_language">
                    Select Language: 
                    <select>
                    <option value="Auto">auto</option>
                        <option value="Assamese">Assamese</option>
                        <option value="Bengali">Bengali</option>
                        <option value="English">English</option>
                        <option value="Gujarati">Gujarati</option>
                        <option value="Hindi">Hindi</option>
                        <option value="Kannada">Kannada</option>
                        <option value="Malayalam">Malayalam</option>
                        <option value="Marathi">Marathi</option>
                        <option value="Punjabi">Punjabi</option>
                        <option value="Sanskrit">Sanskrit</option>
                        <option value="Tamil">Tamil</option>
                        <option value="Telugu">Telugu</option>
                        <option value="Urdu">Urdu</option>
                    </select>
                </div>
            </div>
        )
        
    }
    
}

function YoutubeUploadUI(props) {
    const [YoutubeURL, setYoutubeURL] = useState(''); // Default URL
    const [yt_main, set_yt_main] = useState('');
    const iframeRef = useRef(null);
    const handleYoutubeURL = (event) => {
        // Update the inputValue state when the input value changes
        const patterns = [
            /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/shorts\/)([A-Za-z0-9_-]+)/,
            /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/shorts\/)([A-Za-z0-9_-]+)&/,
        ];
        var match_found = false;
        for (const pattern of patterns) {
            const match = event.target.value.match(pattern);
            if (match && match[1].length == 11) {
                setYoutubeURL(`https://www.youtube.com/embed/${match[1]}`);
                match_found = true;
                iframeRef.current.style.height = "60%";
                set_yt_main(event.target.value);
            }
        }
        if (!match_found) {
            setYoutubeURL("");
            iframeRef.current.style.height = "0px";
        }
    };
    return (
      <div id = "upload_container" className='fill'>
        <div>Paste the YouTube link below to Upload the Song as Base Song.</div>
        <input type="text" placeholder = "Enter YouTube Link Here" onChange={handleYoutubeURL}/>
        <iframe ref = {iframeRef} src={YoutubeURL}></iframe>
        <button onClick={(event)=> {event.target.disabled = true; console.log("YTURL " + YoutubeURL); props.callback(yt_main)}}>Submit</button>
      </div>
    );
}


function AudioPlayer(props) {
    const [audioFile, setAudioFile] = useState(null);
    const audioRef = useRef(null);
    const inputRef = useRef(null);
    const fnameRef = useRef(null);
    const handleDrop = (e) => {
      e.preventDefault();
      const file = e.dataTransfer.files[0];
      handleSelect(file);
    };
    const handleSelect = (file) => {
        if (file && (file.type === 'audio/mpeg' || file.type === 'audio/wav')) {
            setAudioFile(file);
            playAudio(file);

        } 
        else {
            alert('Please upload an MP3 or WAV file.');
        }
    }
    const handleDragOver = (e) => {
      e.preventDefault();
    };

    const playAudio = (file) => {
      const objectURL = URL.createObjectURL(file);
      audioRef.current.src = objectURL;
      audioRef.current.currentTime = 0;
      audioRef.current.pause();
    };
  
    return (
        <div id = "audioupload" className = "full">
            <div onDrop={handleDrop} onDragOver={handleDragOver} onClick = {(e)=>{
                inputRef.current.click();
                inputRef.current.addEventListener('change', function () {
                    if (this.files.length > 0) {
                        handleSelect(this.files[0]);
                    }
                });
                }}>
                <div>Drop Your Audio File Here</div>
                <div>(or)</div>
                <div>Click to Upload File</div>
            </div>
            <audio controls ref={audioRef}/>
            {audioFile?<div style = {{"height": "var(--header-height)"}}>Uploaded File: {audioFile['name']}</div> : ""}
            <button onClick = {(event)=>{event.target.disabled = true; props.callback(audioFile)}}>Submit</button>
            <input ref = {inputRef} type="file" id="audioFileInput" accept=".mp3, .wav" style={{"display": "none"}}></input>
        </div>
      
    );
  }