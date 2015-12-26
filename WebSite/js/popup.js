function showInfo(message, delay, callBack) {
    showToast(message, delay, "info", "mdl-color--green", "mdl-color-text--green", callBack);
}

function showError(message, delay, callBack) {
    showToast(message, delay, "highlight_off", "mdl-color--red", "mdl-color-text--red", callBack);
}

function showToast(message, delay, iconFont, lineColor, textColor, callBack) {
    'use strict';
    var snackbar = document.createElement('div'), text = document.createElement('span'), icon = document.createElement('i'), line = document.createElement('div');
    snackbar.classList.add('mdl-snackbar');
    snackbar.classList.add('mdl-color--white');
    snackbar.classList.add('mdl-shadow--2dp');
    snackbar.classList.add('custom-snack-bar');

    line.classList.add('custom-left-line');
    line.classList.add(lineColor);
    snackbar.appendChild(line);

    icon.classList.add('popup-icon');
    icon.classList.add('material-icons');
    icon.classList.add(textColor);
    icon.innerHTML = iconFont;
    snackbar.appendChild(icon);

    text.classList.add('custom-snack-bar-content');
    text.classList.add(textColor);
    text.innerHTML = message;
    snackbar.appendChild(text);
    document.body.appendChild(snackbar);
    
    setTimeout(function(){
         var height = snackbar.clientHeight;
         snackbar.style.height = 0;
         showHeight(snackbar, height);
    }, 0);
    setTimeout(function(){
        slideToRight(snackbar, 1.0);
    }, delay);
    setTimeout(function(){
        snackbar.remove();
        callBack();
    }, delay + 500);
}


function showHeight(e, to) {
    var height = e.clientHeight + 6;
    if(height > to) height = to;
    e.style.height = height + "px";
    e.style.marginTop = (to - height)/2 + 20 + "px";

    if(height == to) return;

    setTimeout(function() {
        showHeight(e, to);
    }, 10);
}

function slideToRight(e, opacity) {
    //e.style.left = e.offsetLeft + 1 + "px";
    e.style.opacity = opacity;

    if(opacity <= 0) return;
    opacity -= 0.1;
    setTimeout(function() {
        slideToRight(e, opacity);
    }, 20);
}