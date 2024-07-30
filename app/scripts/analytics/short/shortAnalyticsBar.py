from datetime import datetime as dt
from connection import connection_db


def shortAnalyticsBar(request, uid=False):
    try:
        userId = uid if uid else request.user.id
        connection = connection_db()
        dataBase = connection.cursor()
        dataBase.execute(f'select id_user from auth_user where id={userId}')
        id_user = dataBase.fetchall()[0][0]
        dataBase.execute(f'''select id_portfolio from portfolios as p join users as u
    on p.id_enterprise = u.id_enterprise where u.id_user = {id_user}''')
        idPortfolio = dataBase.fetchall()[0][0]
        dataBase.execute(f'select balance_date, balance from balances_history where id_portfolio = {idPortfolio}')
        data = dataBase.fetchall()
        dataBase.close()
        month = [
            'Январь',
            'Февраль',
            'Март',
            'Апрель',
            'Май',
            'Июнь',
            'Июль',
            'Август',
            'Сентябрь',
            'Октябрь',
            'Ноябрь',
            'Декабрь'
        ]
        count = [0] * 10
        for row in data:
            if row[0].year == dt.now().year:
                count[row[0].month - 1] = round(float(row[1]), 2)
        return month, count, sum(count)
    except:
        return 'Error', '', ''