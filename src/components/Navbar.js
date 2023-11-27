import {loadHomepage} from '../navigations'
function Navbar(props) {
    let user_id = localStorage.getItem('capstone_user_id');
    const user_content = 
    (user_id === null) 
    ? 
        <div id = ""></div>
    :
        <button style = {{'backgroundColor': "#fff", 'color': "var(--header-bg)", 'height': "75%", 'fontSize': '18px'}} onClick = {() => {localStorage.removeItem('capstone_user_id'); window.location.assign('/');}}>Logout</button>
    return (
        <header>
            <div onClick={()=>{window.location.assign('/')}}>
                <div id = "header_title">
                    <img src = '/images/image.png' alt = 'icon' href = "/"/>
                    <div>Sruthi Symphony</div>
                </div>
                <div id = "header_user">
                    {user_content}
                </div>
            </div>
        </header>
    )
}

export default Navbar;