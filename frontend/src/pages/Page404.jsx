import '../page404.css'
import image404 from '../images/404.png'
import { useEffect } from 'react'

function doAnimation(image) {
    //יוצר אנימציה על התמונה
    image.classList = []
    void image.offsetHeight;
    image.classList.add('moveUp')

    setTimeout(() => {
        image.classList = []
        void image.offsetHeight;

        image.classList.add('moveDown')
        setTimeout(() => {
            doAnimation(image)

        }, (700))
    }, (700))
}

export default function page404() {
    //מחזיר דף 404

    useEffect(() => {
        fetch('../api/not_404')

        let image = document.getElementById('imageAlive')
        doAnimation(image)
    }, [])
    return (<div className='containerImage'>
        <div className='shadow'></div>
        <img src={image404} alt='image404' id='imageAlive' />
        <p className='text'>page not found error 404</p>
    </div>)
}