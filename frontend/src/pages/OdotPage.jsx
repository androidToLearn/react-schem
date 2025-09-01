import '../odot.css'
import imageTriangle from '../images/t2.png'
import imageStatistica from '../images/s.jpg'
import notLogined from '../images/not_logined.png'
import { Link } from "react-router-dom";
import { useEffect, useState } from 'react';
import '../home.css'
import gmail from '../images/gmail.png'
import whatsapp from '../images/whatssap.webp'




export default function odotPage() {
    //odot page
    const [isLogined, setIsLogined] = useState(false)

    useEffect(() => {

        fetch('http://127.0.0.1:8000/api/hasLogined').then(response => response.json()).then(data => {
            console.log(data)
            if (data['isLogined']) {


                setIsLogined(true)
            }
        })
    }, [])
    return <div className='columnAll' >
        <div className='upLineOdot' style={{ marginTop: '50px', marginLeft: '70px' }}>
            <div className='upLine' style={{ backgroundColor: 'blue' }}>
                <img src={imageTriangle} className='triangle' style={{ position: 'relative', left: '-5px' }} />
                <div className='blueRectangle'></div>
                <img src={imageStatistica} alt='סטטיסטיקה image' className='image' style={{ position: 'absolute', left: '5px' }} />
                <h1 className='title'>vacations data</h1>
                <Link to="/" className='itemMenu' style={{ marginLeft: '500px' }}>Home</Link>
                <div className='seperateLine'></div>
                {!isLogined ?
                    <Link to="/login" className='itemMenu'>Login</Link> :
                    <div className='itemMenu' onClick={() => {
                        fetch('http://127.0.0.1:8000/api/logout').then(resposne => resposne.json()).then(data => {
                            setIsLogined(false)
                        })
                    }}><p className='logout'>Logout</p></div>
                }
                <div className='seperateLine'></div>
                {!isLogined ? <Link to="/login" className='itemMenu' onClick={() => { alert("אינך מחובר") }}>Statistics</Link> : <Link to="/statistics" className='itemMenu'>Statistics</Link>}

                {!isLogined ? <img src={notLogined} /> : <div />}
                <div className='seperateLine'></div>

                <Link to="/odot" className='itemMenu'>Odot</Link>
            </div>
            <div className='whiteLine'></div>
            <div></div>
        </div>
        <div className='containerTextAndLine'>
            <div className='buttonsContact'>
                <div className='whatsapp' >
                    <img src={whatsapp} alt='whatsapp' className='imageContact' onClick={() => {
                        window.open(`https://wa.me/972556880135?text=${encodeURIComponent('')}`, '_blank');

                    }} />

                </div>
                <div className='gmail' >
                    <img src={gmail} alt='gmail' className='imageContact' onClick={() => {
                        let gmailLink = `https://mail.google.com/mail/?view=cm&fs=1&to=rachmutishay@gmail.com&su=${encodeURIComponent('')} &body=${encodeURIComponent('')}`;
                        window.open(gmailLink, '_blank');
                    }} />
                </div>
            </div>
            <div className='myLine'>

            </div>
            <div className='textContainer'>
                <p>שלום זו המערכת לקבלת מידע על המערכת לניהול לייקים על חופשות נוצר על ידי בעזרת react וflask שימוש מהנה.</p>
                <br></br>
                <p>בחסות ישי רחמוט מתכנת full stuck
                </p>
                <br></br>
                <p>לפרטים: טלפון:0556880135</p>
            </div>
            <p className='subText'>בחסות ישי רחמוט</p>

        </div>

    </div>
}