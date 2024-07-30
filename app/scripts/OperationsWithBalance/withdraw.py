from app.scripts.funcs import returnJson, cardValidation
from connection import connection_db
from app.front_app.viewBack.getUserData import getUserData

def withdrawBack(request):
    amount = int(request.POST.get('amount'))
    cardNumber = request.POST.get('card_number')

    errorsDict = cardValidation(amount, cardNumber)

    if errorsDict != {}:
        return returnJson(data=errorsDict)

    user_id = request.user.id
    
    connection = connection_db()
    dataBase = connection.cursor()
    
    dataBase.execute(f'select id_user from auth_user where id={user_id}')
    id_user = dataBase.fetchall()[0][0]

    dataBase.execute(f'select id_enterprise from users where id_user={id_user}')
    id_enterprise = dataBase.fetchall()[0][0]

    dataBase.execute(f'select id_portfolio from portfolios where id_enterprise={id_enterprise}')
    id_portfolio = dataBase.fetchall()[0][0]

    dataBase.execute(f'''insert into operations_history (id_portfolio, oper_type, amount)
values ({id_portfolio}, {False}, {amount})''')
    connection.commit()

    dataBase.execute('select oper_status from operations_history where id_operation = (select max(id_operation) from operations_history)')
    oper_status = dataBase.fetchall()[0][0]

    if oper_status == False:
        errorsDict['message'] = 'Недостаточно свободных средств'
        return returnJson(data=errorsDict)
    
    connection.commit()
    dataBase.close()
    connection.close()

    userData = getUserData(request)

    return returnJson(data={
        'status': 'success',
        'message': 'Успешное снятие',
        'balance': f'{userData['balance']} ₽'
    })