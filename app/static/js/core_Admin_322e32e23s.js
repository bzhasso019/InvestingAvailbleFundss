$('#aUserList').on('click', '.el_hoverer', function(){
    if(pathname[1] == '')
        window.open('/' + $(this).parent().attr('data-type') + '/' + this.getAttribute('data-id'), '_self');
});


if(pathname[1] == 'profile'){
    const inps = document.querySelectorAll('.inputs_bl input');
    $('form#form_profileEdit').on('submit', function(e){
        e.preventDefault();
        if(blocked_button) return;
        blocked_button = true;
        
        if(blocked_button && !errs){
            $('#success_message1, #error_message1').text('');
            let params = $(this).serialize();
            if(pathname[2] != undefined)
                params = $.param({'id': pathname[2]}) + '&' + params;
            urlc = $('#client').length == 0 ? "/editProfile/" : "/editProfileUser/"
            request(urlc, params, function(result){
                try{
                    response = JSON.parse(result);
                    if(response.result == 'fail'){
                        $('#error_message1').text(response.message);
                        $('#success_message1').text('');
                        return;
                    }
                    res = JSON.parse(response.result);
                    if(res['status'] == 'success'){
                        $('#success_message1').text(res.message);
                        $('#error_message1').text('');
                        setTimeout(() => window.location.href = '/profile' + (pathname[2] != undefined ? '/' + pathname[2] : ''), 1500);
                        return;
                    }
                    
                    inps.forEach(item => {
                        if(res[item.id] != undefined) err('.' + item.id, res[item.id]);
                    });

                    $('#error_message1').text(res.message);
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