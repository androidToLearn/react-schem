export default function graphTotalUsersCalculating({ myDataInTotalUsers, setTotalUsers, isInLikes }) {
    //מחשב כמה צריך להיות בprogresstotal
    let totalUsers = 0
    if (!isInLikes) {
        let intervalAddToUsers = setInterval(() => {

            setTotalUsers(totalUsers)
            if (totalUsers === myDataInTotalUsers) {
                console.log('inside')
                clearInterval(intervalAddToUsers)
            }
            totalUsers += 1

        }, 100)
    }
    else {
        let intervalAddToUsers1 = setInterval(() => {

            setTotalUsers(totalUsers)
            if (totalUsers === myDataInTotalUsers) {
                console.log('inside')
                clearInterval(intervalAddToUsers1)
            }
            totalUsers += 1

        }, 10)
    }
}