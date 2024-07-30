const urls = location.pathname;
var blocked_button = false,
    errs = false;

function request(url, requestParams, callback){
    let response = {},
        xhr = new XMLHttpRequest();

    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    blocked_button = true;
    document.body.style.cursor = "wait";
    xhr.onreadystatechange = function(){
        if(xhr.readyState !== 4){
            return;
        }
        if(xhr.status === 200){
            response = {
                result: xhr.responseText,
                description: ""
            };
        }
        else{
            response = {
                result: "fail",
                description: "Ошибка " + xhr.status
            };
            $('#error_message').text('Неожиданная ошибка');
        }
        callback(JSON.stringify(response));
        document.body.style.cursor = "default";
    };
    xhr.send(requestParams);
};

$(document).ready(function() {
    $('#preloader').fadeOut(200);
    setTimeout(() => $('body').removeClass('bpreloader'), 300);
});

var vw = window.innerWidth,
    vh = window.innerHeight;

function inInp(element){
    errs = false;
    let el = $(element.target).parent().parent();
    $(el).removeClass('error');
    $(el).find('.error_podinp').text('');
}

function err(el, val){
    errs = true;
    let interval = 100;
    if(el != 'form'){
        $(el).addClass('error');
        $(el).find('.error_podinp').text(val);
    }
    else{
        $(el).find('#error_message').text(val);
    }
    $(el).animate({left: '-20px'}, interval);
    setTimeout(() => $(el).animate({left: '15px'}, interval), interval);
    setTimeout(() => $(el).animate({left: '-10px'}, interval), interval * 2);
    setTimeout(() => $(el).animate({left: '5px'}, interval), interval * 3);
    setTimeout(() => $(el).animate({left: '0px'}, interval), interval * 4);
    setTimeout(() => blocked_button = false, interval * 5);
}

function clearForm(){
    $('.inputs_bl').removeClass('error');
    $('.error_podinp, .error_messsage, .success_message').text('');
}
function clearInps(){
    $('form input').val('');
}

$('input').on('input', (e) => inInp(e));
$('input').on('change', (e) => inInp(e));