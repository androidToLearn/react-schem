export default function graphUpCalculating({ data, setDataIn3Progresses, isList }) {
    //מחשב כמה צריך להיות בdict כשעולה למעלה
    let biggest = getBiggestValue(data)
    let upToData = []
    let myCopyDataInProgress = {}
    if (isList) {
        for (let i = 0; i < data.length; i++) {
            for (let key in data[i]) {
                myCopyDataInProgress[key] = data[i][key]

            }
        }
        data = myCopyDataInProgress;
        console.log(data)

    }


    for (let key in data) {
        upToData[key] = 0;
    }
    setInterval(() => {
        for (let key in upToData) {
            if (upToData[key] < data[key]) {
                upToData[key] += 1
            }
            setDataIn3Progresses(upToData)
            if (upToData[key] === biggest) {
                clearInterval()
            }
        }
    }, 100)


}

function getBiggestValue(data) {
    //מחזיר את הvalue הכי גבוה בdict
    let biggestValue = 0;
    for (let key in data) {
        if (data[key] > biggestValue) {
            biggestValue = data[key]
        }

    }
    return biggestValue
}