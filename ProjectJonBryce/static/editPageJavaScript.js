document.getElementById('file').addEventListener('change', (event) => {
    //show the chosen image
    let file = event.target.files[0];
    let image = document.getElementById('imageC');

    if (image.classList.contains('imageC2')) {
        image.classList.replace('imageC2', 'imageC');
        let divC = document.getElementById('divImageC')
        divC.style.border = 'none';
    }

    console.log(image);
    image.src = URL.createObjectURL(file);
});

let conic = document.getElementById('divClassConic');
conic.style.display = 'none';


function convertDateToDDMMYYYY(dateStr) {
    //ממיר את הפורמאט לפורמאט הרצוי 12/12/2024
    const date = new Date(dateStr);
    if (isNaN(date)) return ''; // במקרה שהקלט לא תקין

    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0'); // חודשים מתחילים מ-0
    const year = date.getFullYear();

    return `${day}-${month}-${year}`;
}

function clickUpdate(vacationId) {
    //click update or add vacation - update or add the vacation and move to vacations page from edit page
    if (document.getElementById('file').files.length == 0 && !window.isUpdate) {
        alert('choose vacation image')
        return
    }
    let inputs = document.querySelectorAll("input[type='text']")


    console.log(convertDateToDDMMYYYY(inputs[1].value));
    console.log(convertDateToDDMMYYYY(inputs[2].value))

    let e = document.getElementById('myForm');
    let formData = new FormData();
    formData.append('country', inputs[0].value);
    formData.append('description', document.querySelector('textarea').value);
    formData.append('date_start', convertDateToDDMMYYYY(inputs[1].value));
    formData.append('date_end', convertDateToDDMMYYYY(inputs[2].value));
    formData.append('price', inputs[3].value);
    if (document.getElementById('file').files.length > 0) {
        formData.append('file', document.getElementById('file').files[0])
    }
    console.log('fetch...')
    conic.style.display = 'flex';
    document.getElementsByClassName('classShadow')[0].style.height = '1050px'
    fetch('/upload_image/' + vacationId, { method: 'POST', body: formData }).then(response => response.json()).then(data => {
        conic.style.display = 'none';
        document.getElementsByClassName('classShadow')[0].style.height = '950px'


        console.log(data['message'])
        if (data['message'] == 'go') {
            window.location.href = '/go_to_page2';
            console.log('go to page 2')
        }
        else {

            document.getElementById('message').innerText = data['message'];
            document.getElementById('message').style.display = 'block';
        }
    });
}




let classCalanders = document.getElementsByClassName('classCalander');

for (let i = 0; i < classCalanders.length; i++) {
    classCalanders[i].style.display = 'block';
    classCalanders[i].addEventListener('mouseover', () => {
        classCalanders[i].style.backgroundColor = ' rgba(128, 128, 128, 0.221)';
    })

    classCalanders[i].addEventListener('mouseout', () => {
        classCalanders[i].style.backgroundColor = 'white';
    })

    classCalanders[i].addEventListener('click', () => {
        if (i === 0) {

            window.pikaday_start.show(); // פותח את הדיאלוג ידנית

        }
        else {
            window.pikaday_end.show(); // פותח את הדיאלוג ידנית

        }
    })
}

//הצגת היומנים
let classCalanderSource = document.getElementsByClassName('classCalander');
for (let i = 0; i < classCalanderSource.length; i++) {
    classCalanderSource[i].style.display = 'block';
}

function clickCancel() {
    //cancel edit page - go to vacations page
    window.location.href = '/go_to_page2';
}

let arrow_down = document.getElementById('image_arrow');
let block_countries = document.getElementById('block_counries');

let isClicked = false;

//הסתרה והצגת countries menu
document.getElementById('country').addEventListener('click', () => {
    console.log('click')
    if (!isClicked) {
        block_countries.style.top = '190px';
        arrow_down.src = window.up;
        isClicked = true;
    }
    else {
        block_countries.style.top = '-1000px'
        arrow_down.src = window.down;
        isClicked = false;
    }
})




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


block_countries.style.display = 'inline-block';

block_countries.style.top = '-1000px'

//הסתרה  countries menu ביציאה מfocus של הinput

document.getElementById('country').addEventListener('blur', () => {
    setTimeout(() => {
        block_countries.style.top = '-1000px'
        isClicked = false;


    }, 300);
    arrow_down.src = window.down;
})
function initCountries() {
    //init the click on country to be on input
    let countryHovers = document.getElementsByClassName('countryHover');
    for (let i = 0; i < countryHovers.length; i++) {

        countryHovers[i].addEventListener('click', (event) => {
            console.log(event);
            isClicked = false;
            document.getElementById('country').value = countryHovers[i].children[0].innerText;
            document.getElementById('description').focus();
        });
    }
}

initCountries();



//fiter the counties according the text in input
document.getElementById('country').addEventListener('input', () => {

    let value = document.getElementById('country').value;
    isClicked = true;
    block_countries.style.top = '190px';
    arrow_down.src = window.up;


    console.log(value)
    block_countries.innerHTML = ` <div
                                    style="position: relative;width: 310px;height:fit-content;z-index: 5000;overflow: auto;z-index: 1000000;max-hight:300px">`;
    for (let i = 0; i < window.countriesJson.length; i++) {
        console.log(window.countriesJson[i]['name_country'])
        if (window.countriesJson[i]['name_country'].includes(value)) {
            block_countries.innerHTML += ` <div style="border: 1px solid rgb(182, 182, 182);width: 100%;padding: -50px;height: fit-content;text-align: center;z-index: 1000000;cursor: pointer;"
            class="countryHover"> <p>
                ${window.countriesJson[i]['name_country']}
            </p>
        </div>`;
        }
    }
    block_countries.innerHTML += `</div >`;

    initCountries();
});

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


