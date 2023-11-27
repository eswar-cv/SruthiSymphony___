import React, { createRef } from 'react';
function validatePassword(password) {
    // Check length
    if (password.length < 8) {
      return false;
    }
  
    // Check for at least one letter and one digit
    const hasLetter = /[a-zA-Z]/.test(password);
    const hasDigit = /\d/.test(password);
  
    return hasLetter && hasDigit;
  }
export default class Signup extends React.Component {
    // when login procedure is completed a function will be called to move to home page. 
    constructor(props) {
        super(props);
        if (localStorage.getItem("capstone_user_id")) {
            // if valid indicates user exists. move to home page.
            alert("Logout before creating new user.");
            window.location.href = "/home";
        }
        this.validateSignup = this.validateSignup.bind(this);
        this.username = createRef();
        this.password = createRef();
        this.submitbn = createRef();
    }

    validateSignup() {
        this.submitbn.current.disabled = true;
        if (!validatePassword(this.password.current.value)) {
            alert('Password should be atleast 8 characters long and should contain a number.');
            window.location.assign('/signup')
            return
        }
        const data = {
            'user': this.username.current.value,
            'password': this.password.current.value
        }
        fetch(`${this.props.server_url}/validate_signup`, {
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
                window.location.assign('/');
            }
            alert(data['message']);
        })
        .catch((error) => {
            alert("Something went wrong! " + error);
        });
        // this.submitbn.current.disabled = false;
    }
    render() {
        return (
            <div className = 'centerholder'>
                <input ref = {this.username} placeholder='username'></input>
                <input ref = {this.password} type = "password" placeholder='password'></input>
                <button ref = {this.submitbn} onClick={this.validateSignup}>Signup</button>
                <span>Registered User? <a href = "/">Login</a></span>
            </div>
        )
        
    }
}