import React, { createRef } from 'react';
export default class Login extends React.Component {
    // when login procedure is completed a function will be called to move to home page. 
    constructor(props) {
        super(props);
        if (!localStorage.getItem("capstone_user_id")) {
            // if valid indicates user exists. move to home page.
            window.location.href = "/"
        }
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
            <div>

            </div>
        )
        
    }
}

