from connection import connection_db
from app.scripts.mainPages.enterprise.securitiesInfo import securitiesInfo


def analyticsPie(request, uid=False):
    try:
        userId = uid if uid else request.user.id
        connection = connection_db()
        dataBase = connection.cursor()
        pie = {
            'stocks_data': [],
            'bonds_data': [],
            'funds_data': [],
            'curr_metals_data': []
        }
        dataBase.execute(f'select id_user from auth_user where id={userId}')
        id_user = dataBase.fetchall()[0][0]
        dataBase.execute(f'''select id_portfolio from portfolios as p join users as u
    on p.id_enterprise = u.id_enterprise where u.id_user = {id_user}''')
        idPortfolio = dataBase.fetchall()[0][0]
        dataBase.execute(f'select * from portfolio_to_securitie where id_portfolio={idPortfolio}')
        securitiesData = dataBase.fetchall()
        if securitiesData == None:
            dataBase.close()
            connection.close()
            return pie, []
        securitiesData = securitiesInfo(securitiesData)
        dataBase.execute(f'''select total_quantity, quotation, sec_name, ticker, catalog_name, icon
    from portfolio_to_securitie as p join securities as s
    on p.id_securitie = s.id_securitie join catalogs as c
    on s.id_catalog = c.id_catalog where id_portfolio = {idPortfolio}''')
        data = dataBase.fetchall()
        dataBase.close()
        connection.close()
        quantities = {}
        totalSum = 0
        catalogNames = {
            'Акции': 'stocks_data',
            'Облигации': 'bonds_data',
            'Фонды': 'funds_data',
            'Валюта и металлы': 'curr_metals_data'
        }
        for row in data:
            if row[3] != 'RUB':
                idSecuritie = row[2]
                securitieQuantity = float(row[0] * row[1])
                totalSum += securitieQuantity
                quantities[idSecuritie] = (securitieQuantity, row[4], row[5])
        for key in quantities:
            pie[catalogNames[quantities[key][1]]].append(
                {
                    'name': key,
                    'proc': round(quantities[key][0] / totalSum * 100, 2),
                    'count': round(quantities[key][0], 2),
                    'img': quantities[key][2] if quantities[key][2] != None else 'None'
                }
            )
        pie['stocks_data'] = sorted(pie['stocks_data'], key= lambda g: g['name'])
        pie['bonds_data'] = sorted(pie['bonds_data'], key= lambda g: g['name'])
        pie['funds_data'] = sorted(pie['funds_data'], key= lambda g: g['name'])
        pie['curr_metals_data'] = sorted(pie['curr_metals_data'], key= lambda g: g['name'])
        
        securitiesData['stocks_data'] = sorted(securitiesData['stocks_data'], key= lambda g: g['name'])
        securitiesData['bonds_data'] = sorted(securitiesData['bonds_data'], key= lambda g: g['name'])
        securitiesData['funds_data'] = sorted(securitiesData['funds_data'], key= lambda g: g['name'])
        securitiesData['curr_metals_data'] = sorted(securitiesData['curr_metals_data'], key= lambda g: g['name'])
        return pie, securitiesData
    except:
        return 'Error'