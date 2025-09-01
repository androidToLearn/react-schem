import imageStatistica from '../images/s.jpg'
import '../home.css'
import imageTriangle from '../images/t2.png'
import { Link } from "react-router-dom";
import { useEffect, useState } from 'react';
import notLogined from '../images/not_logined.png'
import s from '../images/s.jpeg'
import phone from '../images/phone.jpeg'
import login from '../images/login.webp'


export default function Home() {
    //home page
    const [isLogined, setIsLogined] = useState(false)

    useEffect(() => {

        fetch('../api/hasLogined').then(response => response.json()).then(data => {
            console.log(data)
            if (data['isLogined']) {


                setIsLogined(true)
            }
        })
    }, [])
    return (
        <div className='allContent'>
            <div className='upLine' style={{ backgroundColor: 'blue' }}>
                <img src={imageTriangle} className='triangle' />
                <div className='blueRectangle'></div>
                <img src={imageStatistica} alt='סטטיסטיקה image' className='image' />
                <h1 className='title'>vacations data</h1>
                {!isLogined ?
                    <Link to="/login" className='itemMenu' style={{ marginLeft: '700px' }}>Login</Link> :
                    <div className='itemMenu' style={{ marginLeft: '700px' }} onClick={() => {
                        fetch('http://127.0.0.1:8000/api/logout').then(resposne => resposne.json()).then(data => {
                            setIsLogined(false)
                        })
                    }}>LogOut</div>
                }
                <div className='seperateLine'></div>
                {!isLogined ? <Link to="/login" className='itemMenu' onClick={() => {
                    alert('אינך מחובר')
                }}>Statistics</Link> : <Link to="/statistics" className='itemMenu'>Statistics</Link>}

                {!isLogined ? <img src={notLogined} /> : <div />}
                <div className='seperateLine'></div>

                <Link to="/odot" className='itemMenu'>Odot</Link>
            </div>
            <div className='whiteLine'></div>
            <div className='myTextHome'>
                <p className='titleHomeText' style={{ width: '50%', height: 'fit-content', textAlign: 'end', marginLeft: '-250px', marginTop: '100px' }}>:באפליקציה זו תוכלו לימצוא</p>
                <div className='squaresContainer'>
                    <div className='squares'>
                        <img src={s} alt='image description about the site' className='myImageDescription' />
                        <p className='titleHomeText' style={{ width: '150px', flexWrap: 'wrap', textAlign: 'center' }}>סטטיסטיקות</p>
                    </div>
                    <div className='squares'>
                        <img src={phone} alt='image description about the site' className='myImageDescription' />
                        <p className='titleHomeText' style={{ width: '150px', flexWrap: 'wrap', textAlign: 'center' }}>דף פרטי קשר</p>
                    </div>
                    <div className='squares'>
                        <img src={login} alt='image description about the site' className='myImageDescription' />
                        <p className='titleHomeText' style={{ width: '150px', flexWrap: 'wrap', textAlign: 'center' }}>דף login</p>
                    </div></div>
            </div>
        </div>)
}