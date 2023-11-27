import React, { createRef } from 'react';
navigator.mediaDevices.getUserMedia({ audio: true })
export default class PlayRecord extends React.Component {
    // props - upload_id, url
    constructor(props) {
        super(props);
        this.state = {"audio_chunks": [], "next_state": "Play", "start_point": 0, "end_point": 0, "audio_data": null}; // audio chunks are stored in state of the class
        this.video = createRef();
        this.audio_chunks = [];
        // console.log("startVideo" + this.startVideo);
        this.startVideo = this.startVideo.bind(this);
        this.stopVideo = this.stopVideo.bind(this);
        this.toggleVideo = this.toggleVideo.bind(this);
        this.setStartPoint = this.setStartPoint.bind(this);
        this.setEndPoint = this.setEndPoint.bind(this);
        this.formatTime = this.formatTime.bind(this);
        this.controlVideoEnd = this.controlVideoEnd.bind(this);
        this.setEndPointInit = this.setEndPointInit.bind(this);
        this.startRecording = this.startRecording.bind(this);
        this.stopRecording = this.stopRecording.bind(this);
        this.componentDidMount = this.componentDidMount.bind(this);
        this.submitAudio = this.submitAudio.bind(this);
        this.media_recorder = null;
        this.urlParams = new URLSearchParams(window.location.search);
        this.video_url = `${this.props.server_url}/get_video/${this.urlParams.get('id')}`
    }

    startRecording() {
        // saving the place where the audio started
        document.querySelector("#video_start_point").disabled = true;
        document.querySelector("#video_end_point").disabled = true;
        document.querySelector("#upload_user_audio").disabled = true;
        this.audio_chunks = [];
        let mediaRecorder;
        navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
          this.media_recorder = new MediaRecorder(stream);

          this.media_recorder.ondataavailable = event => {
            if (event.data.size > 0) {
              this.audio_chunks.push(event.data);
            }
          };

          this.media_recorder.onstop = () => {
            const audioBlob = new Blob(this.audio_chunks, { type: 'audio/wav' });
            this.setState({"audio_data": audioBlob});
            const audioURL = URL.createObjectURL(audioBlob);
            document.querySelector("audio").src = audioURL;
          };

          this.media_recorder.start();
        })
        .catch(error => {
          console.error('Error accessing the microphone:', error);
        });
    }

    stopRecording() {
        try {
            this.media_recorder.stop();
        }
        catch {}
        document.querySelector("#video_start_point").disabled = false;
        document.querySelector("#video_end_point").disabled = false;
        document.querySelector("#upload_user_audio").disabled = false;
    }

    formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = parseInt((seconds % 60));
        
        const formattedMinutes = String(minutes).padStart(2, '0');
        const formattedSeconds = String(remainingSeconds).padStart(2, '0');
        return `${formattedMinutes}:${formattedSeconds}`;
    }

    controlVideoEnd() {
        const current_position = this.video.current.currentTime;
        if (current_position >= this.state.end_point && this.state.next_state == "Stop") {
            this.stopVideo();
        } 
    }

    setStartPoint() {
        this.setState({"start_point": this.video.current.currentTime});
        console.log("Set start point as " + this.video.current.currentTime);
    }
    setEndPoint() {
        this.setState({"end_point": this.video.current.currentTime});
        console.log("Set end point as " + this.video.current.currentTime);
    }
    toggleVideo() {
        console.log('toggling video');
        if (this.state.next_state == 'Play') {
            this.startVideo();
        }
        else {
            this.stopVideo();
        }
    }
    startVideo() {
        console.log("Starting Video");
        this.video.current.removeAttribute('controls');
        console.log('startvideo startpoint '+this.state.start_point);
        this.video.current.currentTime = this.state.start_point;
        this.video.current.play();
        this.setState({next_state: "Stop"});
        this.startRecording();
    }
    stopVideo() {
        console.log("Stopping Video");
        this.video.current.setAttribute('controls', 'controls');
        this.video.current.pause();
        this.setState({next_state: "Play"});
        const end_time = this.video.current.currentTime;
        this.stopRecording();
    }
    setEndPointInit(video_obj) {
        this.setState({'end_point': this.video.current.duration});
        this.video.current.addEventListener('timeupdate', this.controlVideoEnd);
    }
    componentDidMount() {
        this.video.current.addEventListener('ended', this.stopVideo)
        this.video.current.addEventListener('paused', this.stopVideo);
        this.video.current.onloadedmetadata = this.setEndPointInit;
    }
    submitAudio() {
        // send post request to Flask server
        // should contain song_id, song_details
        
        if (!this.state.audio_data) {
            alert("Play Video to record Audio before Uploading.")
        }
        else {
            const form_data = new FormData();
            form_data.append("start_point", this.state.start_point);
            form_data.append("end_time", this.state.end_point);
            form_data.append("audio", this.state.audio_data, "user_input.wav");
            
            fetch(`${this.props.server_url}/upload_audio`, {
                method: 'POST',
                body: form_data
            }).then(response => {
                if (response.ok) { // response is okay
                    const data = response.json();
                    data.then(
                        res=> {
                            if (res['status']) {
                                
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
        }
        
    // VideoHolder contains the video
    // Controlsholder contains video start and stop buttons, video start and stop seekers
    render() {
        return (
            <div id = "PlayRecord">
                <div id = "VideoHolder">
                    <video preload="metadata" ref = {this.video} id = "playvideo" src = {this.video_url} controls></video>
                </div>
                <div id = "ControlsHolder">
                    <button id = "video_pp" onClick={this.toggleVideo} style = {{"backgroundColor": (this.state.next_state == "Play"?"#41B566":"#FF6D4D")}}>{this.state.next_state}</button>
                    <div className='setTimeDisplay'>Start: {this.formatTime(this.state.start_point)}</div>
                    <button id = "video_start_point" className = "setTimeReset" onClick={this.setStartPoint}>Set</button>
                    <div className='setTimeDisplay'>End: {this.formatTime(this.state.end_point)}</div>
                    <button id = "video_end_point" className = "setTimeReset" onClick={this.setEndPoint}>Set</button>
                    <audio controls></audio>
                    <button id = "upload_user_audio" onClick={this.submitAudio}>Submit Audio</button>
                </div>
            </div>
        )
        
    }
    
}

