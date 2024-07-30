from connection import connection_db


def shortAnalyticsBalance(request, uid=False):
    try:
        userId = uid if uid else request.user.id
        connection = connection_db()
        dataBase = connection.cursor()
        dataBase.execute(f'select id_user from auth_user where id={userId}')
        id_user = dataBase.fetchall()[0][0]
        dataBase.execute(f'''select id_portfolio from portfolios as p join users as u
    on p.id_enterprise=u.id_enterprise where u.id_user={id_user}''')
        idPortfolio = dataBase.fetchall()[0][0]
        dataBase.execute(f'select balance, deposition from portfolios where id_portfolio={idPortfolio}')
        data = dataBase.fetchall()[0]
        balance = float(data[0])
        deposition = float(data[1])
        balancePercent = '0'
        if deposition:
            balancePercent = str(round(100 * balance/deposition - 100, 2))
        if balancePercent[0] != '-':
            balancePercent = '+' + balancePercent
        return balance, balancePercent
    except:
        return 'Error', ''