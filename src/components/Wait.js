import React, { createRef } from 'react';
export default class Wait extends React.Component {
    // when login procedure is completed a function will be called to move to home page. 
    constructor(props) {
        super(props);
        let urlParams = new URLSearchParams(window.location.search);
        this.state = {'id': urlParams.get('id'), 'message': 'Waiting to process audio.'}
        this.componentDidMount = this.componentDidMount.bind(this);
        this.refresh = this.refresh.bind(this);
        }
    refresh() {
        console.log('refreshing');
        fetch(`${this.props.server_url}/wait_status/${this.state.id}`)
            .then((response) => response.json())
            .then((data) => {
                console.log('data ' + JSON.stringify(data));
                if (data['status'] == 'done') {
                    // alert( JSON.stringify(data));
                    
                    window.location.assign(`/view_and_record?id=${data['video_id']}&base_audio_id=${data['base_audio_id']}`);
                }
                else {
                    this.setState({'message': data['message']});
                }
            })
            .catch((error) => {console.log('something went wrong. Please try again later.')});
    }
    componentDidMount() {
        setInterval(()=>{
            this.refresh()
        }, 5000)
    }
    render() {
        return (
            <div id = "Wait" style={{ whiteSpace: 'pre-wrap', 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center' }}>
                {this.state.message}
            </div>
        )
        
    }
}