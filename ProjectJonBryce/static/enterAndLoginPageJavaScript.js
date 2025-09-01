//defualt values to search vacation by json
fetch('/send_search_json', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id: '-1', country: '-1', description: '-1', price: '-1', ischeaked: '-1', month_start: '-1', year_start: '-1', days_vacation: '-1' }) });


let divClassConic = document.getElementById('divClassConic');
divClassConic.style.display = 'none';

document.getElementById('message').style.display = 'none';

function clickClassEnter() {
    //from login or register page - enter to vacations page if is good or show relevant message
    document.getElementById('message').style.display = 'none';




    let allTexts = document.querySelectorAll("input[type='text']");
    console.log(allTexts);
    if (allTexts.length == 4) {
        divClassConic.style.display = 'block';

        fetch('/in_like_page', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ 'name': allTexts[0].value, 'second_name': allTexts[1].value, 'password': allTexts[2].value, 'email': allTexts[3].value }) }).then(response => {

            return response.json();

        })
            .then(data => {
                if (data['message'].length !== 0) {
                    if (data['message'] === 'go') {
                        window.location.href = '/go_to_page2';
                        divClassConic.style.display = 'none';

                    }
                    else {
                        divClassConic.style.display = 'none';

                        document.getElementById('message').innerText = data['message']
                        document.getElementById('message').style.display = 'block';
                    }
                }


            });
    }
    else {
        divClassConic.style.display = 'block';

        fetch('/in_like_page', {
            method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ 'password': allTexts[1].value, 'email': allTexts[0].value })
        }).then(response => {
            divClassConic.style.display = 'block';

            return response.json();

        })
            .then(data => {
                if (data['message'].length !== 0) {

                    if (data['message'] === 'go') {
                        window.location.href = '/go_to_page2';
                        divClassConic.style.display = 'none';

                    }
                    else {
                        divClassConic.style.display = 'none';

                        document.getElementById('message').innerText = data['message']
                        document.getElementById('message').style.display = 'block';
                    }



                }

            });
    }
}

function moveProgress() {
    //there is a progress that show when I do enter
    let classConic = document.getElementsByClassName('classConic')[0];
    let progress = 0;
    setInterval(() => {
        classConic.style.setProperty('--progress1', progress);
        progress += 5;
        progress = progress % 101;
    }, 100);
}

moveProgress();

//על מנת שלא יסתיר דברים חשובים ולחיצות block_countries מהmenu
document.getElementById('block_counries').style.display = 'none';

//הסתרת היומנים מהmenu
let classCalanderSource = document.getElementsByClassName('classCalander');
for (let i = 0; i < classCalanderSource.length; i++) {
    classCalanderSource[i].style.display = 'none';
}

try {
    //טוען את התפריט לחופשות
    let divVication = document.getElementById('divVication');
    divVication.addEventListener('click', () => {
        divClassConic.style.display = 'block';
        console.log('go to page 2')

        fetch('/in_like_page').then(response => response.json()).then(data => {
            window.location.href = '/go_to_page2';
            console.log('in page 2')
            divClassConic.style.display = 'none';
        });
    })

}
catch (error) {
    //טוען תפריט לחופשות בלי הרשמה למערכת
    let divNoRLvication = document.getElementById('divNoRLvication');
    divNoRLvication.addEventListener('click', () => {
        divClassConic.style.display = 'block';

        console.log('go to page 2 without permission')
        fetch('/in_like_page').then(response => response.json()).then(data => {
            window.location.href = '/go_to_vacation_page_without_login_or_register';
            console.log('in page 2 without permission')
            divClassConic.style.display = 'none';


        });
    })
}