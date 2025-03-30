let teacher = document.getElementById('teacher');
let student = document.getElementById('student');
let result = document.getElementById('result');
let select = document.getElementById('content');
let teacherup = document.getElementById('teacherupload');
let studentup = document.getElementById('studentupload');
let btn = document.getElementById('recognizeButton');
let serverUrl = 'http://localhost:5000/run_my_script';

btn.addEventListener("click", postfunction);

function scrollToResult() {
    document.querySelector('.result-section').scrollIntoView({ 
        behavior: 'smooth',
        block: 'center'
    });
}

function postfunction() {
    let selectValue = select.value;
    
    // Don't proceed if image/video is selected (under development)
    if (selectValue !== "text") {
        result.textContent = 'This feature is currently under development.';
        result.style.color = '#dc3545';
        scrollToResult();
        return;
    }

    let inputData;
    let headers = {};

    if (selectValue === "text") {
        inputData = JSON.stringify({
            teacherans: teacher.value,
            studentans: student.value
        });
        headers['Content-Type'] = 'application/json';
    } else {
        inputData = new FormData();
        inputData.append("teacherans", teacherup.files[0]);
        inputData.append("studentans", studentup.files[0]);
    }

    result.textContent = 'Calculating The Result....';
    result.style.color = 'var(--text-color)';
    scrollToResult();

    fetch(serverUrl, {
        method: 'POST',
        headers: headers,
        body: inputData,
    })
    .then(function (response) {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Request failed.');
        }
    })
    .then(function (data) {
        result.textContent = data['result'];
    })
    .catch(function (error) {
        console.error(error);
        result.textContent = 'Error occurred while processing your request.';
        result.style.color = '#dc3545';
    });
}



