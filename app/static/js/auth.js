const nameInput = {
    'role': 'Роль',
    'username': 'Логин',
    'email': 'Почту',
    'password': 'Пароль',
    'title': 'наименование организации',
    'typeProperty': 'вид собственности',
    'address': 'адрес главного офиса',
    'name': 'ФИО',
    'phone': 'Номер телефона'
}

$('input').on('input', (e) => inInp(e));
$('input').on('change', (e) => inInp(e));

$(document).ready(function() {
    const inps = document.querySelectorAll('.inputs_bl input');
    
    $('#password').keydown(function(event) {
      if (event.keyCode == 13) $('#auth_but, #reg_but').click();
    });
    
    $('form#auth_form').on('submit', function(e){
        e.preventDefault();
        if(blocked_button) return;
        clearForm();

        blocked_button = true;
        inps.forEach(item => {
            if(item.value.trim() == '') err('.' + item.id, 'Введите ' + nameInput[item.id]);
        });
        
        if(blocked_button && !errs){
            let params = $(this).serialize();
            request("/login/", params, function(result){
                try{
                    response = JSON.parse(result);
                    if(response.result == 'fail'){
                        err('form', response.description);
                        return;
                    }
                    res = JSON.parse(response.result);
                    if(res['status'] == 'success'){
                        window.location.href = '/';
                        clearForm();
                        blocked_button = false;
                        return;
                    }

                    err('form', res.message);
                    blocked_button = false;
                }
                catch(e){
                    err('form', 'Неожиданная ошибка');
                }
            });
        }
        blocked_button = false;
    });

    $('form#registration_form').on('submit', function(e){
        e.preventDefault();
        if(blocked_button) return;
        clearForm();

        blocked_button = true;
        inps.forEach(item => {
            if(item.value.trim() == '') err('.' + item.id, 'Введите ' + nameInput[item.id]);
        });
        
        if(blocked_button && !errs){
            let params = $.param({'login': $('#email').val()}) + '&' + $(this).serialize();
            request("/reg/", params, function(result){
                try{
                    response = JSON.parse(result);
                    if(response.result == 'fail'){
                        err('form', response.description);
                        return;
                    }
                    res = JSON.parse(response.result);
                    if(res['status'] == 'success'){
                        window.location.href = '/';
                        clearForm();
                        blocked_button = false;
                        return;
                    }
                    
                    inps.forEach(item => {
                        if(res[item.id] != undefined) err('.' + item.id, res[item.id]);
                    });
                    blocked_button = false;
                }
                catch(e){
                    err('form', 'Неожиданная ошибка');
                }
            });
        }
        blocked_button = false;
    });
});