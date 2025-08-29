import '../statsticsPage.css'


export default function graphUpView({ myDataIn3Progresses }) {
    //מחזיר את הview של הdict
    return <div className='contentDiagramUp'>
        {Object.entries(myDataIn3Progresses).map((oneUpData, index) => {
            return <div key={index} className='oneProgress'>
                <p style={{ margin: '5px', color: 'white' }}>{oneUpData[0]}: {oneUpData[1]}</p>
                <div style={{ height: `${(oneUpData[1] / 100) * 200}px` }} className='theInsideBoxProgress'></div>
            </div>
        })}
    </div>
}