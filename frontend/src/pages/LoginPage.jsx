import { useEffect, useState, } from "react"
import '../login.css'
import key from '../images/key.png'
import men from '../images/men.png'
import { useNavigate } from "react-router-dom"


export default function login() {
    //login page
    const [message, setMessage] = useState('');
    const navigate = useNavigate()
    return (<form className="box" onSubmit={(event) => {
        event.preventDefault()
        let userInput = document.getElementById('user')
        let passwordInput = document.getElementById('password')
        console.log('send request to login...')
        fetch('../api/login', {
            method: 'post', headers: { 'Content-Type': 'application/json' }, credentials: 'include',
            body: JSON.stringify({ 'name': userInput.value, 'password': passwordInput.value })
        }).then(response => response.json()).then(data => {
            if (data['message'] === 'logined!') {
                document.getElementById('message').style.color = 'green'
                navigate('/statistics')
            }
            setMessage(data['message'])
            console.log('send message')
        })
    }}>
        <h1 >דף היתחברות</h1>
        <label htmlFor="user" style={{ marginTop: '100px' }} >user</label>
        <input type="text" id="user" name="user" autoComplete="user" placeholder="user..." className="input" />
        <img src={men} className="icon" />
        <label htmlFor="password">password</label>
        <input type="password" id="password" name="password" autoComplete="password" placeholder="password..." className="input" />
        <img src={key} className="icon" />
        <p className="message" id="message">{message}</p>
        <div className="btnContainer">
            <input type="submit" value={'Login'} className="btnLogin" />
        </div>

    </form>)
}