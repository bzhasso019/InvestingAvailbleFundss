from connection import connection_db

def history(request, uid=False):
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
    
        dataBase.execute(f'select id_enterprise from Users where id_user={id_user}')
        id_enterprise = dataBase.fetchall()[0][0]
        dataBase.execute(f'select id_portfolio from Portfolios where id_enterprise={id_enterprise}')
        id_portfolio = dataBase.fetchall()[0][0]
        dataBase.execute(f'select * from Operations_History where id_portfolio={id_portfolio}')
        operations = dataBase.fetchall()
    
        data = []
    
        if operations == None:
            dataBase.close()
            connection.close()
            return data
        for operation in operations:
            operationType = operation[1]
            operationStatus = operation[2]
            operationDate = operation[3].strftime('%d.%m.%Y %H:%M')
            operationAmount = float(operation[4])
            if operationAmount == int(operationAmount):
                operationAmount = int(operationAmount)
    
            if(operationStatus):
                operationTypes = ['Вывод', 'Пополнение']
                operationData = {
                    'type': operationTypes[int(operationType)],
                    'date': operationDate,
                    'price': operationAmount
                }
                data.append(operationData)
        dataBase.close()
        connection.close()
        return [name, data[::-1]]
    except:
        return ['', 'Error']