// 'use strict';

function handleLikeClick() {
    console.log('Кнопка лайка нажата');
}

let button = document.querySelector("#like-button");
button.addEventListener("click", handleLikeClick);


