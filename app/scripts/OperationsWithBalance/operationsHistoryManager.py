from connection import connection_db
from app.scripts.OperationsWithBalance.operationsHistory import history
from datetime import datetime as dt


def historyManager(request, uid=False):
    try:
        
        id = uid if uid else request.user.id

        connection = connection_db()
        dataBase = connection.cursor()

        dataBase.execute(f"select id_user from auth_user where id={id}")
        id_user = dataBase.fetchall()[0][0]

        dataBase.execute(f'select id_employee from Users where id_user={id_user}')
        id_employee = dataBase.fetchall()[0][0]

        dataBase.execute(f'select id_portfolio from Portfolios where id_employee={id_employee}')
        portfoliosId = dataBase.fetchall()

        data = []

        if portfoliosId == None:
            dataBase.close()
            connection.close()
            return data
        for portfolio in portfoliosId:
            id_portfolio = portfolio[0]

            dataBase.execute(f'select id_enterprise from Portfolios where id_portfolio={id_portfolio}')
            enterpriseId = dataBase.fetchall()[0][0]

            dataBase.execute(f'select id_user from Users where id_enterprise={enterpriseId}')
            idUserClient = dataBase.fetchall()[0][0]

            dataBase.execute(f'select id from auth_user where id_user={idUserClient}')
            uid = dataBase.fetchall()[0][0]

            operationInfo = history(request, uid)
            operationInfo.append(uid)
            data.append(operationInfo)
        
        data2 = []
        
        for i in data:
            for j in i[1]:
                j['date'] = dt.strptime(j['date'], '%d.%m.%Y %H:%M')
                data2.append({
                    'id': i[2],
                    'name': i[0],
                    'operation': j
                })
        data2.sort(key= lambda g: g['operation']['date'], reverse=True)

        for i in data2:
            i['operation']['date'] = i['operation']['date'].strftime('%d.%m.%Y %H:%M')

        dataBase.close()
        connection.close()
        return data2
    except:
        return 'Error'