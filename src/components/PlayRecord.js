import { toHaveDisplayValue } from '@testing-library/jest-dom/matchers';
import React, { createRef } from 'react';
navigator.mediaDevices.getUserMedia({ audio: true })
export default class PlayRecord extends React.Component {
    // props - upload_id, url
    constructor(props) {
        super(props);
        this.state = {"audio_chunks": [], "next_state": "Play", "start_point": 0, "end_point": 0, "audio_data": null, 'tbc': 'Base Audio'}; // audio chunks are stored in state of the class
        this.video = createRef();
        this.base_audio = createRef();
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
        this.toggle_video_base_audio = this.toggle_video_base_audio.bind(this);
        this.media_recorder = null;
        this.urlParams = new URLSearchParams(window.location.search);
        this.video_url = `${this.props.server_url}/get_video/${this.urlParams.get('id')}`;
        this.base_audio_url = this.urlParams.get('base_audio_id');
        console.log('BASE_AUDIO_ID')
        console.log(this.base_audio_url)
        this.audio_source = 'video';
        this.setEndPointInit = this.setEndPointInit.bind(this);
        this.tbc = 'Base Audio';
        if (this.base_audio_url != 'undefined' && this.urlParams.get('base_audio_id') != '' && this.urlParams.get('base_audio_id') != 'null') {
            this.view_type = "report";
            this.tbc = 'Base Audio';
            this.base_audio_fetch_url = `${this.props.server_url}/get_audio/${this.urlParams.get('base_audio_id')}`;
        }
        else {
            this.tbc = 'Video';
            this.view_type = "base";
        }
    }

    toggle_video_base_audio(event) {
        console.log(this.tbc);
        if (this.audio_source == 'video') { // change audio source to audio
            // mute video
            this.video.current.muted = true;
            this.base_audio.current.muted = false;
            this.audio_source = 'base_audio';
            this.setState({'tbc': 'Video'});
        }
        else {
            this.video.current.muted = false;
            this.base_audio.current.muted = true;
            this.audio_source = 'video';
            this.setState({'tbc': 'Base Audio'});
        }
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
            document.querySelector("#audio_user").src = audioURL;
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
        if (this.video.current.duration - current_position < 0.1) {
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
        if (this.urlParams.get('base_audio_id')) {
            document.querySelector("#video_start_point").disabled = true;
            document.querySelector("#video_end_point").disabled = true;
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
        console.log('setting end ' + this.video.current.duration + this.video.current)
        this.setState({'end_point': this.video.current.duration});
        this.video.current.addEventListener('timeupdate', this.controlVideoEnd);
    }
    syncPlay = () => {
        // Play both the audio and video elements if one of them is played
        const audio = this.base_audio.current;
        const video = this.video.current;
      
        if (!audio.paused) {
          video.play();
        }
        if (!video.paused) {
          audio.play();
        }
      }
      
      syncPause = () => {
        // Pause both the audio and video elements if one of them is paused
        const audio = this.base_audio.current;
        const video = this.video.current;
      
        if (audio.paused) {
          video.pause();
        }
        if (video.paused) {
          audio.pause();
        }
      }
      
      syncSeek = () => {
        // When one of the elements is seeked, sync the current time of the other to match
        this.base_audio.current.currentTime = this.video.current.currentTime;
      }
    componentDidMount() {
        
        this.setEndPointInit();
        if (this.urlParams.get('base_audio_id') != 'undefined' && this.urlParams.get('base_audio_id') != '' && this.urlParams.get('base_audio_id') != 'null') {
            this.video.current.addEventListener('ended', this.stopVideo);
            this.video.current.addEventListener('paused', this.stopVideo);
            this.video.current.onloadedmetadata = this.setEndPointInit;

            this.base_audio.current.addEventListener('play', this.syncPlay);
            this.base_audio.current.addEventListener('pause', this.syncPause);
            // this.base_audio.current.addEventListener('seeked', this.syncSeek);

            this.video.current.addEventListener('play', this.syncPlay);
            this.video.current.addEventListener('pause', this.syncPause);
            this.video.current.addEventListener('seeked', this.syncSeek);
            document.querySelector("#video_start_point").disabled = true;
            document.querySelector("#video_end_point").disabled = true;
        }
        
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
            form_data.append("base_audio", this.urlParams.get('base_audio_id'));
            form_data.append("video_id", this.urlParams.get('id'));
            fetch(`${this.props.server_url}/upload_audio`, {
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
        }
        
    // VideoHolder contains the video
    // Controlsholder contains video start and stop buttons, video start and stop seekers
    render() {
        return (
            <div id = "PlayRecord">
                <div id = "VideoHolder">
                    <video ref = {this.video} id = "playvideo" src = {this.video_url} controls></video>
                </div>
                <div id = "ControlsHolder">
                    <button id = "video_pp" onClick={this.toggleVideo} style = {{"backgroundColor": (this.state.next_state == "Play"?"#41B566":"#FF6D4D")}}>{this.state.next_state}</button>
                    <div className='setTimeDisplay'>Start: {this.formatTime(this.state.start_point)}</div>
                    <button id = "video_start_point" className = "setTimeReset" onClick={this.setStartPoint}>Set</button>
                    <div className='setTimeDisplay'>End: {this.formatTime(this.state.end_point)}</div>
                    <button id = "video_end_point" className = "setTimeReset" onClick={this.setEndPoint}>Set</button>
                    <audio id = "audio_user" controls></audio>
                    <button id = "upload_user_audio" onClick={this.submitAudio}>Submit Audio</button>
                    {this.view_type == 'report' ? <audio ref = {this.base_audio} controls muted src = {this.base_audio_fetch_url}></audio> : ""}
                    {this.view_type == 'report' ? <button onClick = {this.toggle_video_base_audio}>Change Audio Source to {this.state.tbc}</button> : ""}
                </div>
            </div>
        )
        
    }
    
}

