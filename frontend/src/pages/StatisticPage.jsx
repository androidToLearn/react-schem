import '../statsticsPage.css'
import { useState, useEffect } from 'react'
import fillGraphUp from '../components/GraphUpCalculating.jsx'
import { data } from 'react-router-dom'
import graphUpView from '../components/GrahpUpView.jsx'
import graphTotalUsersCalculating from '../components/GraphTotalUserCaculatning.jsx'
import graphTotalUsersView from '../components/GraphTotalUsersView.jsx'
import edit from '../images/edit.png'
import { jsx } from 'react/jsx-runtime'

function getFuturesCountriesAndLikesByNumDays(date, setPredictedCountriesAndLikes, setIsProgress, setIsEditClicked, setNumDays
) {
    //מעדכן את גרף ה
    //  futeure likes and vacations
    //לאחר input עוד כמה ימים
    const today = new Date(); // התאריך הנוכחי
    const selectedDate = new Date(date); // התאריך מהinput
    const diffTime = selectedDate - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    if (diffDays < 0) {
        alert('past date')
        return
    }
    setNumDays(diffDays)

    setIsEditClicked(false)
    setIsProgress(true)
    fetch('../api/futureLikes', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ 'days': diffDays, 'month': -1, 'years': -1 }) })
        .then(response => response.json()).then(data => {
            setIsProgress(false)
            setPredictedCountriesAndLikes(data)
        })

}


function getFuturesCountriesAndLikesByNumDaysInit(numDays, setPredictedCountriesAndLikes, setIsProgress
) {
    //כמו הפונקציה למעלה רק בערך defualt של עוד 30 ימים
    setIsProgress(true)
    fetch('../api/futureLikes', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ 'days': numDays, 'month': -1, 'years': -1 }) })
        .then(response => response.json()).then(data => {
            setIsProgress(false)
            setPredictedCountriesAndLikes(data)
        })

}

export default function statistics() {
    //statistics page
    let [myDataIn3Progresses, setDataIn3Progresses] = useState({ numPast: 0, numOnGoing: 0, numFuture: 0 })
    let [myDataInTotalUsers, setTotalUsers] = useState(0)
    let [myDataInTotalLikes, setTotalLikes] = useState(100)
    let [myDataInCountiesProgress, setDataContries] = useState({})
    let [predictedCountiesAnLikes, setPredictedCountriesAndLikes] = useState({ futureVacations: 0, futureLikes: 0 })
    let [totalCountries, setTotalCountries] = useState(0)
    let [numDays, setNumDays] = useState(30)
    let [isEditClicked, setIsEditClicked] = useState(false);
    let [isProgress, setIsProgress] = useState(false)
    const now = new Date();
    let [date, setDate] = useState(now.toISOString().split("T")[0])


    window.document.body.addEventListener('click', () => {
        setIsEditClicked(false)
    })

    useEffect(() => {
        fetch('../api/vacations/stats').then(response => response.json()).then(data => {
            //    return {"pastVacations": numBefore, "ongoingVacations": numCurrent, "futureVacations": numFuture}
            fillGraphUp({ data: data, setDataIn3Progresses: setDataIn3Progresses, isList: false })
        })

        fetch('../api/users/total').then(response => response.json()).then(data => {
            //{'totalUsers': numUsers}
            graphTotalUsersCalculating({ myDataInTotalUsers: data['totalUsers'], setTotalUsers: setTotalUsers, isInLikes: true })
        })

        fetch('../api/likes/total').then(response => response.json()).then(data => {
            graphTotalUsersCalculating({ myDataInTotalUsers: data['totalLikes'], setTotalUsers: setTotalLikes, isInLikes: true })
        })
        fetch('../api/likes/distribution').then(response => response.json()).then(data => {
            fillGraphUp({ data: data, setDataIn3Progresses: setDataContries, isList: true })
        })

        fetch('../api/sumCountries').then(response => response.json()).then(data => {
            setTotalCountries(data['sumCountries'])
        })

        //numDays, setPredictedCountriesAndLikes, setIsProgress
        getFuturesCountriesAndLikesByNumDaysInit(30, setPredictedCountriesAndLikes, setIsProgress)

    }, [])
    return (<div>
        <div className='upLineStatistics'>
            <h1 className='titleStatistics'>נתונים על המערכת לניהול לייקים</h1>
        </div>
        <div className='content'>
            <div className='oneRow'>
                <div className="oneDiagrama">
                    <div className='boxDiagramaAndTitle'>
                        <p className='titleDiagrama1' >נתונים על חופשות</p>
                        <div className='boxDiagramUp'>

                            {graphUpView({ myDataIn3Progresses: myDataIn3Progresses })
                            }

                            <div className='blueBaseLine'>

                            </div>
                        </div>
                    </div>

                </div>

                <div className="oneDiagrama">
                    <div className='boxDiagramaAndTitle'>
                        <p style={{ color: 'white' }} >totalUsers</p>
                        {graphTotalUsersView({ myDataInTotalUsers: myDataInTotalUsers, color: `rgba(198, 214, 76, 1)`, text: `100 יש ${myDataInTotalUsers}  מיתוך משתמשים` })}

                    </div>

                </div>
            </div>

            <div className='oneRow'>
                <div className="oneDiagrama">
                    <div className='boxDiagramaAndTitle' style={{ paddingBottom: '300px' }}>
                        <p style={{ color: 'white' }} >totalLikes</p>
                        {graphTotalUsersView({ myDataInTotalUsers: myDataInTotalLikes, color: `rgb(11, 163, 183)`, text: ` 100  יש ${myDataInTotalLikes} מיתוך לייקים` })}
                    </div>

                </div>

                <div className="oneDiagrama">
                    <div className='boxDiagramaAndTitle'>
                        <p className='titleDiagrama1' >לייקים על הארצות</p>
                        {myDataInTotalLikes !== 0 ? <div className='boxDiagramUp'>
                            {graphUpView({ myDataIn3Progresses: myDataInCountiesProgress })
                            }

                            <div className='blueBaseLine'>

                            </div>
                        </div> : <p className='titleDiagrama1' >אין לייקים</p>}


                    </div>

                </div>
            </div>

            <div className='oneRow' style={{ paddingBottom: '100px' }}>
                <div className="oneDiagrama">
                    <div className='boxDiagramaAndTitle'>
                        <img src={edit} alt='editImage' className='imageEdit' onClick={(e) => {
                            e.stopPropagation()
                            setIsEditClicked(true)
                        }} />
                        {isEditClicked ? <div className='editContainer' onClick={(e) => {
                            e.stopPropagation()
                        }}>
                            <label htmlFor="date" className="instructionedit">בחר תאריך:</label>
                            <input
                                id="date"
                                type="date"
                                value={date}
                                onChange={(e) => { setDate(e.target.value) }}
                                className="calendarEdit"
                            />
                            <p className="resultEdit">התאריך שנבחר: {date.toString()}</p>
                            <input type='button' className='btnEdit' value={'done'} onClick={(e) => {
                                getFuturesCountriesAndLikesByNumDays(date, setPredictedCountriesAndLikes, setIsProgress, setIsEditClicked, setNumDays)
                            }} />
                        </div> : <div />}
                        <p className='titleDiagrama1' >vacations and likes predictor more {numDays}</p>
                        <div className='boxDiagramUp'>

                            {graphUpView({ myDataIn3Progresses: predictedCountiesAnLikes })
                            }

                            <div className='blueBaseLine'>

                            </div>
                        </div>
                    </div>

                </div>

                <div className="oneDiagrama">
                    <div className='boxDiagramaAndTitle'>
                        <p style={{ color: 'white' }} >total countries</p>
                        {graphTotalUsersView({ myDataInTotalUsers: totalCountries, color: `rgba(64, 221, 95, 1)`, text: ` 100  יש ${totalCountries} מיתוך ארצות` })}

                    </div>

                </div>
            </div>
        </div>
    </div>)
}