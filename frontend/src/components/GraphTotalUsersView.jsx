import '../statsticsPage.css'

export default function graphTotalUsersView({ myDataInTotalUsers, color, text }) {
    //מחזיר את הprogress total view
    return <div className='allGraph2'><div className='conic' style={{
        background: `conic-gradient(${color} 0% ${myDataInTotalUsers}%, white ${myDataInTotalUsers}% 100%)`
    }}></div>
        <div className='centerCircle'>

            <p className='centerText'>{text}</p>

        </div>
    </div>
}