// used to change the UI
// no changes should be done to index.js unless mandatory
import logo from './logo.svg';
import './App.css';
import './BasicConfig.css';
import {Navbar, Footer, Login, Signup, PlayRecord, UploadAudio, Wait, Home} from './components';
import './navigations.js';
import './videoplayer.css';
import './uploadaudio.css';
import './general.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

const ServerURL = "http://127.0.0.1:8000";
// const ServerURL = "https://264347d9469fb9147804cc08e572cacf.loophole.site";
// https://rw8js2r9-8000.inc1.devtunnels.ms/
const WebPage = (props) => {
    return ( 
        <div id = "Container">
            <Navbar></Navbar>
            {props.content}
            <Footer></Footer>
        </div>
    )
}

function App() {
    return (
        <Router>
            <Routes>
                <Route exact path = "/" element = {<WebPage content = {<Login server_url = {ServerURL}/>}></WebPage>}/>
                <Route path = "/home" element = {<WebPage content = {<Home server_url = {ServerURL}/>}></WebPage>}/>
                <Route path = "/wait" element = {<WebPage content = {<Wait server_url = {ServerURL}/>}></WebPage>}/>
                <Route path = "/signup" element = {<WebPage content = {<Signup server_url = {ServerURL}/>}></WebPage>}/>
                <Route path = "/upload" element = {<WebPage content = {<UploadAudio server_url = {ServerURL}/>}></WebPage>}/>
                <Route path = "/view_and_record" element = {<WebPage content = {<PlayRecord server_url = {ServerURL}/>}></WebPage>}/>
            </Routes>
        </Router>
    )
}
export default App;