if(['payment', 'withdraw'].indexOf(pathname[1]) !== -1){
    const inps = document.querySelectorAll('.inputs_bl input');
    $('.auth_inp_o_num').on('keyup, input', function(e){
        let val = $('.auth_inp_o_num').val().replace(/[^0-9]/g, '').substr(0, 16).replace(/(.{4})/g, '$1 ').trim();
        $('.auth_inp_o_num').val(val);
    });
    $('.auth_inp_o_date').on('keyup, input', function(e){
        let val = $('.auth_inp_o_date').val().replace(/[^0-9]/g, '').substr(0, 4).replace(/(\d{2})(\d{2})/g, '$1/$2').trim();
        $('.auth_inp_o_date').val(val);
    });


    $('form#doPayment').on('submit', function(e){
        e.preventDefault();
        if(blocked_button) return;
        clearForm();

        blocked_button = true;
        if($('#amount').val().trim() == '') err('.amount', 'Введите сумму пополнения');
        if($('#card_number').val().trim() == '') err('.card_number', 'Введите номер карты');
        if($('#card_date').val().trim() == '') err('.card_date', 'Введите срок карты');
        if(blocked_button && !errs){
            let params = $(this).serializeArray();
            params.forEach(function(item){
                item.value = item.value.replace(/[^0-9/]/g, '');
            });
            params = $.param(params);
            request("/refillBtn/", params, function(result){
                try{
                    response = JSON.parse(result);
                    if(response.result == 'fail'){
                        err('form', response.description);
                        return;
                    }
                    res = JSON.parse(response.result);
                    if(res['status'] == 'success'){
                        clearForm();
                        clearInps();
                        $('#error_message').text('');
                        $('#success_message').text(res.message);
                        blocked_button = false;
                        return;
                    }
                    
                    inps.forEach(item => {
                        if(res[item.id] != undefined) err('.' + item.id, res[item.id]);
                    });
                    
                    if(res.message){
                        err('form', res.message)
                    }

                    blocked_button = false;
                }
                catch(e){
                    err('form', 'Неожиданная ошибка');
                }
            });
        }
        blocked_button = false;
    });
    

    $('form#doWithdraw').on('submit', function(e){
        e.preventDefault();
        if(blocked_button) return;
        clearForm();

        blocked_button = true;
        if($('#amount').val().trim() == '') err('.amount', 'Введите сумму вывода');
        if($('#card_number').val().trim() == '') err('.card_number', 'Введите номер карты');
        if(blocked_button && !errs){
            let params = $(this).serializeArray();
            params.forEach(function(item){
                item.value = item.value.replace(/[^0-9/]/g, '');
            });
            params = $.param(params);
            request("/withdrawBtn/", params, function(result){
                try{
                    response = JSON.parse(result);
                    if(response.result == 'fail'){
                        err('form', response.description);
                        return;
                    }
                    res = JSON.parse(response.result);
                    if(res.status == 'success'){
                        clearForm();
                        clearInps();
                        $('#error_message').text('');
                        $('#success_message').text(res.message);
                        $('#amount').attr('placeholder', res.balance);
                        blocked_button = false;
                        return;
                    }
                    
                    inps.forEach(item => {
                        if(res[item.id] != undefined) err('.' + item.id, res[item.id]);
                    });
                    
                    if(res.message){
                        err('form', res.message)
                    }

                    blocked_button = false;
                }
                catch(e){
                    err('form', 'Неожиданная ошибка');
                }
            });
        }
        blocked_button = false;
    });
}

if(pathname[1] == 'profile'){
    $('#deleteProfile').on('click', function(){
        if(blocked_button) return;
        blocked_button = true;
        
        if(blocked_button && !errs){
            $('#success_message, #error_message').text('');
            request("/deleteProfile/", '', function(result){
                try{
                    response = JSON.parse(result);
                    if(response.result == 'fail'){
                        $('#error_message').text(response.message);
                        $('#success_message').text('');
                        return;
                    }
                    res = JSON.parse(response.result);
                    if(res['status'] == 'success'){
                        $('#success_message').text(res.message);
                        $('#error_message').text('');
                        setTimeout(() => window.location.href = '/auth/', 1500);
                        return;
                    }
                    
                    $('#error_message').text(res.message);
                    blocked_button = false;
                }
                catch(e){
                    err('form', 'Неожиданная ошибка');
                }
            });
        }
        blocked_button = false;
    });
}