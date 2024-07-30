from connection import connection_db
from app.scripts.funcs import returnJson, fti


def getAdditionalInfo(dataBase, idSecuritie, idPortfolio):
    dataBase.execute(f'select quotation from securities where id_securitie={idSecuritie}')
    quotation = fti(dataBase.fetchall()[0][0])
    dataBase.execute(f'select total_quantity from portfolio_to_securitie where id_portfolio={idPortfolio} and id_securitie={idSecuritie}')
    portfolioPrice = fti(dataBase.fetchall()[0][0]) * quotation
    dataBase.execute(f'select quotation from queue where id_securitie={idSecuritie} and id_portfolio={idPortfolio} order by queue_date')
    try:
        oldPrice = dataBase.fetchall()[0][0]
        
        proc = 100 - (float(oldPrice)/float(quotation))*100
    except:
        proc = 0
    return [portfolioPrice, proc]
    

def tradeAction(request):
    ticker = request.POST.get('ticker')
    action = bool(int(request.POST.get('action')))
    quantity = request.POST.get('quantity')
    userId = request.POST.get('uid')

    if not(quantity) or quantity == '0':
        return returnJson(status='error', message='Введите количество')

    connection = connection_db()
    dataBase = connection.cursor()
    
    dataBase.execute(f'select id_securitie from securities where ticker=\'{ticker}\'')
    id_securitie = dataBase.fetchall()[0][0]

    dataBase.execute(f'select id_user from auth_user where id={userId}')
    id_user = dataBase.fetchall()[0][0]
    dataBase.execute(
        f'select id_portfolio from portfolios as p join users as u on p.id_enterprise=u.id_enterprise where u.id_user={id_user}')
    id_portfolio = dataBase.fetchall()[0][0]

    if action:
        dataBase.execute(
            f'insert into requests (id_portfolio, id_securitie, quantity, req_type) values ({id_portfolio}, {id_securitie}, {quantity}, true)')

        connection.commit()

        dataBase.execute(f'select req_status from requests where id_request = (select max(id_request) from requests)')
        oper_status = dataBase.fetchall()[0][0]

        if not (oper_status):
            dataBase.close()
            connection.close()
            return returnJson(status='error', message='Недостаточно свободных средств')

        dataBase.execute(f'select total_quantity from portfolio_to_securitie where id_portfolio={id_portfolio} and (id_securitie={id_securitie} or id_securitie=36) order by id_securitie')
        fetchs = dataBase.fetchall()
        newTotalQuantity = fetchs[0][0]
        newBalance = fetchs[1][0]
        info = getAdditionalInfo(dataBase, id_securitie, id_portfolio)
        dataBase.close()
        connection.close()
        return returnJson(data={
            'total_quantity': fti(newTotalQuantity),
            'balance': fti(newBalance),
            'status': 'success',
            'message': 'Покупка совершена успешно',
            'total_sum': info[0],
            'proc': info[1]
        })

    dataBase.execute(f'insert into requests (id_portfolio, id_securitie, quantity, req_type) values ({id_portfolio}, {id_securitie}, {quantity}, false)')
    connection.commit()
    dataBase.execute(f'select req_status from requests where id_request = (select max(id_request) from requests)')
    oper_status = dataBase.fetchall()[0][0]

    if not (oper_status):
        dataBase.close()
        connection.close()
        return returnJson(status='error', message='Указано неверное колличество для продажи')

    dataBase.execute(f'select total_quantity from portfolio_to_securitie where id_portfolio={id_portfolio} and (id_securitie={id_securitie} or id_securitie=36) order by id_securitie')
    fetchs = dataBase.fetchall()
    if len(fetchs) == 2:
      newBalance = fetchs[1][0]
      newTotalQuantity = fetchs[0][0]
    else:
      newBalance = fetchs[0][0]
      newTotalQuantity = 0
    if newTotalQuantity > 0:
        info = getAdditionalInfo(dataBase, id_securitie, id_portfolio)
    else:
        info = [0, 0]
    dataBase.close()
    connection.close()
    return returnJson(data={
        'total_quantity': fti(newTotalQuantity),
        'balance': fti(newBalance),
        'status': 'success',
        'message': 'Продажа совершена успешно',
        'total_sum': info[0],
        'proc': info[1]
    })