from connection import connection_db
from .securitiesInfo import *
from app.scripts.funcs import fti


def enterpriseMainPage(request, uid=False):
    try:
        id = uid if uid else request.user.id
        name = ''

        connection = connection_db()
        dataBase = connection.cursor()
    
        dataBase.execute(f'select id_user, first_name, last_name, patronymic from auth_user where id={id}')
        data = dataBase.fetchall()[0]
        id_user = data[0]
        if uid:
            name += f'{data[2]} {data[1][0]}.'
            if data[3] != None:
                name += f' {data[3][0]}.'

        dataBase.execute(f'select id_enterprise from users where id_user={id_user}')
        data = dataBase.fetchall()[0]
        id_enterprise = data[0]

        dataBase.execute(f'select * from portfolios where id_enterprise={id_enterprise}')
        data = dataBase.fetchall()[0]
        balance = data[1]
        deposition = data[3]
        id_portfolio = data[0]
        balanceChange = balance - deposition
        balanceChangePercentage = 0
        if deposition != 0:
            balanceChangePercentage = float(balanceChange) / (float(deposition) * 0.01)

        balanceInfo = {
            'balance': fti(balance),
            'var_balance': fti(balanceChange),
            'balance_proc': fti(balanceChangePercentage)
        }

        data = balanceInfo

        dataBase.execute(f'select * from portfolio_to_securitie where id_portfolio={id_portfolio}')
        securities = dataBase.fetchall()

        if securities == None:
            dataBase.close()
            connection.close()
            return data

        balanceData = securitiesInfo(securities)
        dataBase.close()
        connection.close()
        return data, balanceData, name
    except:
        return ['', '', 'Error']