import React, { createRef } from 'react';
export default class Home extends React.Component {
    // when login procedure is completed a function will be called to move to home page. 
    constructor(props) {
        super(props);
        if (!localStorage.getItem("capstone_user_id")) {
            // if valid indicates user exists. move to home page.
            window.location.href = "/"
        }
        this.componentDidMount = this.componentDidMount.bind(this);
        this.state = {'user_table': '', 'user_name': ''}
    }

    componentDidMount() {
        fetch(`${this.props.server_url}/get_user_data/${localStorage.getItem("capstone_user_id")}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            this.setState({"user_table": <TableComponent data = {data}/>})
            this.setState({'user': data.user})
        })
        .catch((error) => {
            alert("Something went wrong! " + error);
        });
    }

    validateLogin() {
        this.submitbn.current.disabled = true;
        const data = {
            'user': this.username.current.value,
            'password': this.password.current.value
        }
        fetch(`${this.props.server_url}/validate_login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            if (data['status'] == 'done') {
                localStorage.setItem('capstone_user_id', data['id']);
                window.location.assign('/');
            }
            alert(data['message']);
        })
        .catch((error) => {
            alert("Something went wrong! " + error);
        });
        this.submitbn.current.disabled = false;
    }
    render() {
        return (
            <div id = "HomePage" className = 'fill'>
                <h2>Welcome {this.state['user']}!</h2>
                <button onClick={()=>{window.location.assign('/upload')}}>Upload song</button>
                {this.state['user_table']}
            </div>
        )
        
    }
}

const TableComponent = (props) => {
    // Given data structure
    const data = props.data
  
    // Combine both base_audios and report_audios for the table
    const combinedData = data['audios']
  
    return (
        (combinedData.length > 0)?
      <table>
        <thead>
          <tr>
            <th>_id</th>
            <th>Type</th>
            <th>Video ID</th>
          </tr>
        </thead>
        <tbody>
          {combinedData.map((audio, index) => (
            <tr key={index} onClick = {(event) => {window.location.href = `/view_and_record?id=${audio.video_id}&base_audio_id=${(audio.type == 'base')?'':audio._id}`}}>
              <td>{audio._id}</td>
              <td>{audio.type}</td>
              <td>{audio.video_id}</td>
            </tr>
          ))}
        </tbody>
      </table>:<h2>No Songs Uploaded, Yet.</h2>
    );
  }