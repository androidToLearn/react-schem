
let divClassConic = document.getElementById('divClassConic');
let divUp = document.getElementById('divUp');
let divAll = document.getElementById('divAll');
divClassConic.style.display = 'none';
let isClickOnDeleteOrEditOrLike = false;


let isSomethingChanged = false;
if (performance.navigation.type === 1) {
    //if there is an action for example add like and in the same time I do refresh the action will be bad , therefore I destroy the refresh and after the add like action I do refresh
    divClassConic.style.display = 'block';
    divUp.style.height = '240px';
    let interval = setInterval(() => {
        if (!isSomethingChanged) {
            fetch('/in_like_page', { method: 'POST' }).then(response => response.json()).then(data => {
                if (data['message'] === 'go') {
                    console.log('go to page 2')
                    window.location.href = '/go_to_page2';

                }
            });
            clearInterval(interval);
        }
    }, 100);
}

function doGoodClickOnCheckBoxes(div, vacationid, usr_id, isHasPermission) {
    //init clicking on like button to vacation
    isClickOnDeleteOrEditOrLike = true;
    console.log('isHasPermission' + isHasPermission)
    if (isHasPermission) {
        isSomethingChanged = true;
        console.log(isSomethingChanged);
        if (div.children[1].style.color === 'gray') {
            div.children[0].src = window.red;
            div.children[1].innerText = 'Likes ' + (getNumber(div.children[1].innerText) + 1);
            div.children[1].style.color = 'black';
            clickAddLike(vacationid, usr_id);
            div.style.backgroundColor = 'rgb(255, 197, 196)';
        }
        else {
            div.children[0].src = window.gray;
            div.children[1].innerText = 'Likes ' + ((getNumber(div.children[1].innerText) - 1));
            div.children[1].style.color = 'gray';

            clickRemoveLike(vacationid, usr_id);
            div.style.backgroundColor = 'whitesmoke';
        }
    }
    else {
        window.location.href = '/'
    }

    setTimeout(() => {
        isClickOnDeleteOrEditOrLike = false;
    }, 1000);
}

function getNumber(innerText) {
    //get number from string 'innerText'
    let string = '';
    for (let i = 0; i < innerText.length; i++) {
        if (innerText[i] >= '0' && innerText[i] <= '9') {
            string += innerText[i];
        }
    }
    return parseInt(string);
}


function clickAddLike(vacationid, usr_id) {
    //in add like action do view changes and server data changes
    isClickOnDeleteOrEditOrLike = true;

    fetch('/likes_page', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ 'id_vacation': vacationid, 'id_user': usr_id }) }).then(response => response.json()).then(data => {
        isSomethingChanged = false;
        console.log(isSomethingChanged);
        setTimeout(() => {
            isClickOnDeleteOrEditOrLike = false;
        }, 1000)
    });;
}

function clickRemoveLike(vacationid, usr_id) {
    //in remove like do view changes and server data changes
    isClickOnDeleteOrEditOrLike = true;

    fetch('/likes_page_delete', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ 'id_vacation': vacationid, 'id_user': usr_id }) }).then(response => response.json()).then(data => {
        isSomethingChanged = false;
        console.log(isSomethingChanged);
        setTimeout(() => {
            isClickOnDeleteOrEditOrLike = false;
        }, 1000)
    });
}

let alertDialog = document.getElementsByClassName('alertDialog');
let idGray = document.getElementById('idGray');
idGray.style.display = 'none';

//here init click on gray when I open alertDialog
idGray.addEventListener('click', () => {
    isClickOnDeleteOrEditOrLike = true;
    hideAlert();
    setTimeout(() => {
        isClickOnDeleteOrEditOrLike = false;
    }, 1000)
});

function hideAllAlerts() {
    //init alerts to be hidden
    alertDialog[0].style.display = 'none';
    idGray.style.display = 'none';

}


let keepCountry = null;
let keepId = null;
let text = document.getElementById('textQ');

function hideAlert() {

    //alert that opened - hide it
    alertDialog[0].style.display = 'none';
    idGray.style.display = 'none';
}
hideAllAlerts();

function showAlertDialog(index, country, id, isHasPermission) {
    //show alert dialog are you want to delete
    if (isHasPermission) {
        keepCountry = country;
        keepId = id;


        isClickOnDeleteOrEditOrLike = true;

        text.innerText = ` would you like
                to
                delete the vacation to ` + country + ' ?';
        alertDialog[0].style.display = 'block';
        idGray.style.display = 'block';

        setTimeout(() => {
            isClickOnDeleteOrEditOrLike = false;
        }, 1000)
    }
    else {
        window.location.href = '/'
    }
}

function click_update_vacation(vacation_id, isHasPermission) {
    //go to update vacation page
    if (isHasPermission) {
        isClickOnDeleteOrEditOrLike = true;

        window.location.href = '/go_to_editPage/' + vacation_id;
        setTimeout(() => {
            isClickOnDeleteOrEditOrLike = false;
        }, 1000);
    }
    else {
        window.location.href = '/';
    }
}

let allTexts = document.getElementsByClassName('editTextClass');
let checkLike = document.getElementsByClassName('divLike');
let realCheck = document.getElementsByClassName('cheackboxclass');
let bt = document.getElementById('m');
let buttons_search = document.getElementsByClassName('button_search');

function restartAll() {
    //hide all search fields and radioButtons field
    for (let i = 0; i < allTexts.length; i++) {
        allTexts[i].style.display = 'none';
    }
    checkLike[0].style.display = 'none';
}

function clickSomeSearchButton(indexButton) {
    //clicking on some search filed and show him
    console.log(indexButton);
    restartAll();
    doUnderLine(indexButton);
    if (indexButton === 4) {
        checkLike[0].style.display = 'block';
    }
    else if (indexButton > 4) {
        //the allTexts is length -1 from button_search therefore button index minus 1
        indexButton = indexButton - 1;
        allTexts[indexButton].style.display = 'block';
    }
    else {
        allTexts[indexButton].style.display = 'block';
    }
}

function doUnderLine(indexButton) {
    //show under line under the button of the current search field
    let all = document.getElementsByClassName('under_line');

    for (let i = 0; i < all.length; i++) {
        all[i].style.display = 'none';
    }

    all[indexButton].style.display = 'block'
}

function doClickOnButtons() {
    //init clicks for buttons of search fields
    for (let i = 0; i < buttons_search.length; i++) {

        buttons_search[i].addEventListener('click', (event) => {
            console.log(i)

            clickSomeSearchButton(i);
        });

        buttons_search[i].addEventListener('mouseover', (event) => {
            console.log('over')
            buttons_search[i].style.backgroundColor = 'rgb(128 , 128 , 128 , 0.32)';
        });

        buttons_search[i].addEventListener('mouseout', (event) => {
            buttons_search[i].style.backgroundColor = 'transparent';
        });
    }
}


function clickDelete() {
    isClickOnDeleteOrEditOrLike = true;
    divClassConic.style.display = 'block';
    divUp.style.height = '240px';

    //click delete vacation
    fetch('/delete_vacation/' + keepId).then(response => response.json()).then(data => {
        if (data['message'] == 'go') {
            console.log('go to page 2')
            window.location.href = '/go_to_page2';
            divClassConic.style.display = 'none';
            divUp.style.height = 'fir-content';
            setTimeout(() => {
                isClickOnDeleteOrEditOrLike = false;
            }, 1000)
        }
    });
}



function doDefaultValues() {
    //init values on search fields when I enter to the page again 
    fetch('/get_search_json')
        .then(response => response.json())
        .then(data => {
            if (data.id != '-1') {
                allTexts[0].value = data.id;
                console.log(data.id);
            }
            if (data.country != '-1') {
                allTexts[1].value = data.country;
            }
            if (data.description != '-1') {
                allTexts[2].value = data.description;
            }
            if (data.price != '-1') {
                allTexts[3].value = data.price;
            }
            if (data.ischeaked !== '-1') {
                if (data.ischeaked === '1') {
                    realCheck[0].checked = true;
                }
                else if (data.ischeaked === '2') {
                    realCheck[1].checked = true;
                }
                else {
                    realCheck[2].checked = true;
                }
            }
            else {
                realCheck[2].checked = true;
            }
            if (data.month_start != '-1') {
                allTexts[4].value = data.month_start;
            }
            if (data.year_start != '-1') {
                allTexts[5].value = data.year_start;
            }
            if (data.days_vacation != '-1') {
                allTexts[6].value = data.days_vacation;
            }
        });
}


function doGoodClickOnCheacks() {
    //in the search I init the radioButtons properly

    for (let i = 0; i < realCheck.length; i++) {
        realCheck[i].addEventListener('click', () => {
            realCheck[0].checked = false;
            realCheck[1].checked = false;
            realCheck[2].checked = false;
            realCheck[i].checked = true;
        });
    }
}

doDefaultValues();//init with the default values
clickSomeSearchButton(0);//the search start with id field filtering
doClickOnButtons();//init clicking for id field and other search fields 
doGoodClickOnCheacks();//init the radioButton (isLike and not like)
bt.style.display = 'none';



function clickSearchDo() {
    //init click search button
    divClassConic.style.display = 'block';
    divUp.style.height = '240px';
    bt.style.display = 'block';

    let id = allTexts[0].value.trim();
    if (id.length === 0) {
        id = '-1';
    }
    let country = allTexts[1].value.trim();
    if (country.length === 0) {
        country = '-1';
    }
    let description = allTexts[2].value.trim();
    if (description.length === 0) {
        description = '-1';
    }
    let price = allTexts[3].value.trim();
    if (price.length === 0) {
        price = '-1';
    }
    let numChecked = '-1';
    if (realCheck[0].checked) {
        numChecked = '1';
    }
    else if (realCheck[1].checked) {
        numChecked = '2';
    }
    else if (realCheck[2].checked) {
        numChecked = '3';
    }
    let month_start = allTexts[4].value.trim();
    if (month_start.length === 0) {
        month_start = '-1';
    }
    let year_start = allTexts[5].value.trim();
    if (year_start.length === 0) {
        year_start = '-1';
    }
    let days_vacation = allTexts[6].value.trim();
    if (days_vacation.length === 0) {
        days_vacation = '-1';
    }

    myjson = { id: id, country: country, description: description, price: price, ischeaked: numChecked, month_start: month_start, year_start: year_start, days_vacation: days_vacation };

    document.getElementById('m').innerText = 'loading ... please wait';
    document.getElementById('m').style.color = 'blue';

    fetch('/send_search_json', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(myjson) })
        .then(response => response.json())
        .then(data => {
            if (data['message'] == 'go') {
                window.location.href = '/go_to_page2';
                divClassConic.style.display = 'none';
                divUp.style.height = 'fit-content';
            }
            else {
                document.getElementById('m').innerText = data['message']
                document.getElementById('m').style.color = 'red';
                divClassConic.style.display = 'none';
                divUp.style.height = 'fit-content';
            }
        });
}


function moveProgress() {
    //move some progress that appear when I click on search button
    let classConic = document.getElementsByClassName('classConic')[0];
    let progress = 0;
    setInterval(() => {
        classConic.style.setProperty('--progress1', progress);
        progress += 5;
        progress = progress % 101;
    }, 100);
}

moveProgress();


function clickShowDescription(description, image_name, title) {
    //for clicking on vacation
    if (!isClickOnDeleteOrEditOrLike) {
        window.location.href = '/go_to_description_page/' + description + '/' + image_name + '/' + title;
    }
}


try {
    //טוען את התפריט לחופשות
    let divVication = document.getElementById('divVication');
    divVication.addEventListener('click', () => {
        divClassConic.style.display = 'block';

        divUp.style.height = '240px';

        console.log('go to page 2')

        fetch('/in_like_page').then(response => response.json()).then(data => {
            window.location.href = '/go_to_page2';
            console.log('in page 2')
            divClassConic.style.display = 'none';
            divUp.style.height = 'fit-content';

        });
    })

}
catch (error) {
    //טוען תפריט לחופשות בלי הרשמה למערכת
    let divNoRLvication = document.getElementById('divNoRLvication');
    divNoRLvication.addEventListener('click', () => {
        divClassConic.style.display = 'block';
        divUp.style.height = '240px';


        console.log('go to page 2 without permission')
        fetch('/in_like_page').then(response => response.json()).then(data => {
            window.location.href = '/go_to_vacation_page_without_login_or_register';
            console.log('in page 2 without permission')
            divClassConic.style.display = 'none';
            divUp.style.height = 'fit-content';



        });
    })
}

//על מנת שלא יסתיר דברים חשובים ולחיצות block_countries מהmenu
document.getElementById('block_counries').style.display = 'none';

//הסתרת היומנים מהmenu
let classCalanderSource = document.getElementsByClassName('classCalander');
for (let i = 0; i < classCalanderSource.length; i++) {
    classCalanderSource[i].style.display = 'none';
}
divClassConic.style.display = 'none';
divUp.style.height = 'fit-content';