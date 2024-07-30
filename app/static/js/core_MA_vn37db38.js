if(['', 'employee'].indexOf(pathname[1]) !== -1){
    const cloneClientBlock = $('.cloneClientBlock').clone();
    $('.cloneClientBlock').remove();
        
    $('#hnewClient').on('click', function(){
        if(!blocked_button){
            blocked_button = true;
            $('.newClientEmail').toggleClass('activeh');
            $('.newClientEmail').animate({
                height: "toggle"
            }, 500, function(){
                blocked_button = false;
                if(!$('.newClientEmail').hasClass('activeh')){
                    $('#error_message, #success_message').text('');
                    $('.auth_inp_o').val('');
                }
            });
        }
    });

    $('form#mAddEmail_form').on('submit', function(e){
        e.preventDefault();
        if(blocked_button) return;
        clearForm();

        blocked_button = true;
        if($('#email').val().trim() == '') err('.email', 'Введите email');
        
        if(blocked_button && !errs){
            let params = new URLSearchParams();
            params.append('email', $('#email').val());
            if(pathname[2] != undefined)
                params.append('id', pathname[2]);
            request("/mAddClientMail/", params, function(result){
                try{
                    response = JSON.parse(result);
                    if(response.result == 'fail'){
                        err('form', response.description);
                        return;
                    }
                    res = JSON.parse(response.result);
                    if(res['status'] == 'success'){
                        clearForm();
                        $('#email').val('');
                        $('#error_message').text('');
                        $('#success_message').text(res.message);

                        let html = cloneClientBlock.html()
                        .replace('$id', res.id)
                        .replace('$name', res.name)
                        .replace('$balance', res.balance)
                        .replace('$balance_proc', res.balance_proc)
                        .replace('$color', (toString(res.balance_proc).includes("-")) ? 'col_red' : 'col_lb');
                        $('#mClientsList').prepend(html);
                        $('.cloneb').fadeIn(400);
                        setTimeout(() => $('.cloneb').removeClass('cloneb'), 400);

                        setTimeout(function(){
                            $('#hnewClient').click()
                            blocked_button = false;
                            setTimeout(() => $('#success_message').text(''), 500);
                        }, 600);
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
}

if(pathname[1] == 'trade'){
    $('.trade_tabs').on('click', '.el_hoverer', function(){
        window.open('/securitiesTrade/' + pathname[2] + '/' + this.getAttribute('data-id'), '_self');
    });
    
    $('button').on('click', function(){
        if(!blocked_button){
            blocked_button = true;
            let thiss = this;
            let tid = this.getAttribute('data-tab');
            $('button').removeClass('back_lb');
            $('.tabs').fadeOut(200);
            setTimeout(function(){
                $(thiss).addClass('back_lb');
                $('[data-tabId="' + tid + '"]').fadeIn(200);
                setTimeout(() => blocked_button = false, 200);
            }, 200);
        }
    });
}

$('#mClientsList').on('click', '.el_hoverer', function(){
    if(['', 'operations', 'employee'].indexOf(pathname[1]) !== -1)
        window.open('/enterprise/' + this.getAttribute('data-id'), '_self');
});

function resizeHe(){
    if(['operations', 'tradeHistory'].indexOf(pathname[1]) !== -1){
        $('.nomh > div > div:nth-child(2)').css('max-height', 'calc(100vh - ' + ($('.header').height() + $('nav').height() + $('.nomh > div > div.h1').height()) + 'px - 11.5rem)');
    }
    if(pathname[1] == 'trade'){
        $('.nomh > div > div:nth-child(2)').css('max-height', 'calc(100vh - ' + ($('.header').height() + $('nav').height() + $('.tradeSels').height() + $('.nomh > div > div.h1').height()) + 'px - 14rem)');
    }
}
resizeHe();

function resizeSaleSum(){
    if(pathname[1] == 'securitiesTrade'){
        sale_sum = $('.trade_sale_sum').width();
        $('.inp_bl input').css('padding-right', 'calc(' + sale_sum + 'px + 3rem)');
    }
}
resizeSaleSum();


window.addEventListener('resize', (e) => {
    if(window.innerWidth == vw && window.innerHeight == vh && !isResize) return;
    vw = window.innerWidth;
    vh = window.innerHeight;
    resizeHe();
    resizeSaleSum();
    isResize = false;
});


if(pathname[1] == 'securitiesTrade'){
    var trade_value = ''
    function dynamicSumTrade(){
        if(blocked_button) return;
        blocked_button = true;

        let inp_val = $('#salse_sum').val().replace(/[^0-9]/g, '');
        
        if(blocked_button && !errs && inp_val != trade_value){
            trade_value = inp_val;
            let params = new URLSearchParams();
            params.append('ticker', pathname[3]);
            params.append('quantity', inp_val != '' ? inp_val : 0);
            request("/tradeSum/", params, function(result){
                try{
                    response = JSON.parse(result);
                    if(response.result == 'fail'){
                        err('form', response.description);
                        return;
                    }
                    res = JSON.parse(response.result);
                    if(res['status'] == 'success'){
                        $('.trade_sale_sum').text(res['message'])
                    }
                    blocked_button = false;
                }
                catch(e){
                    err('form', 'Неожиданная ошибка');
                }
            });
        }
        blocked_button = false;
    }

    $('.sale_buy_but button').on('click', function(){
        if(blocked_button) return;
        blocked_button = true;
        
        if(blocked_button && !errs){
            $('#success_message, #error_message').text('');
            let params = new URLSearchParams();
            params.append('uid', pathname[2]);
            params.append('ticker', pathname[3]);
            params.append('action', $(this).attr('data-type') == 'buy' ? 1 : 0);
            params.append('quantity', $('#salse_sum').val().replace(/[^0-9]/g, ''));
            request("/tradeBtn/", params, function(result){
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
                        $('#trade_balance').text(res['balance']);
                        $('#total_quantity').text(res['total_quantity']);
                        $('#total_sum').text(res['total_sum']);
                        $('#proc').text(res['proc'] + '%');
                        $('.auth_inp_o_sum').val('')
                        $('.trade_sale_sum').text('0 ₽')
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
    })

    $('#salse_sum').on('input', (e) => dynamicSumTrade(e));
    $('#salse_sum').on('change', (e) => dynamicSumTrade(e));
}

if(pathname[1] == 'enterprise'){
    $('#unlinkClient').on('click', function(){
        if(blocked_button) return;
        blocked_button = true;
        
        if(blocked_button && !errs){
            $('#success_message, #error_message').text('');
            let params = new URLSearchParams();
            params.append('uid', pathname[2]);
            request("/unlinkClient/", params, function(result){
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
                        setTimeout(() => window.location.href = '/', 1500);
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