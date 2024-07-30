from connection import connection_db
from app.scripts.funcs import returnJson, cardValidation

def refillBack(request):
    amount = int(request.POST.get('amount'))
    cardNumber = request.POST.get('card_number')
    cardDateInput = request.POST.get('card_date').split('/')
    
    errorsDict = cardValidation(amount, cardNumber, cardDateInput)
    
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
values ('{id_portfolio}', {True}, {amount})''')
    connection.commit()
    dataBase.close()
    connection.close()

    return returnJson(status='success', message='Успешное пополнение')
