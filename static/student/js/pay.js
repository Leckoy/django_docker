'use strict';

function go_to_pay() {
    window.location = 'http://localhost:8000/student/pay/';
}

let button = document.querySelector("#go_to_pay");
button.addEventListener("click", go_to_pay);