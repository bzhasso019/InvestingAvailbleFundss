from connection import connection_db
from app.scripts.funcs import fti

def trading_history(uid):
    connection = connection_db()
    dataBase = connection.cursor()

    dataBase.execute(f"select id_user from auth_user where id={uid}")
    idUserClient = dataBase.fetchall()[0][0]

    dataBase.execute(f"select id_enterprise from users where id_user={idUserClient}")
    idEnterprise = dataBase.fetchall()[0][0]

    dataBase.execute(f"select id_portfolio from portfolios where id_enterprise={idEnterprise}")
    idPortfolio = dataBase.fetchall()[0][0]

    dataBase.execute(f"select id_securitie, req_type, req_status, quantity, req_date, total_price from requests where id_portfolio={idPortfolio}")
    requestsInfo = dataBase.fetchall()

    data = []

    for request in requestsInfo:
        if(request[2]):
            idSecuritie = request[0]
            requestsTypes = ['Продажа', 'Покупка']
            requestType = requestsTypes[int(request[1])]
            quantity = request[3]
            requestDate = request[4]
            totalPrice = request[5]
            dataBase.execute(f"select sec_name, ticker, icon from securities where id_securitie='{idSecuritie}'")
            securitie = dataBase.fetchall()[0]
            securitieName = securitie[0]
            ticker = securitie[1]
            iconPath = securitie[2]
            requestInfo = {
                'name': securitieName,
                'short_name': ticker,
                'img': iconPath,
                'type': requestType,
                'price': fti(totalPrice),
                'count': fti(quantity),
                'datetime': requestDate,
                'date': requestDate.strftime('%d.%m.%Y'),
                'time': requestDate.strftime('%H:%M')
            }
            data.append(requestInfo)

    if data:
        data.sort(key=lambda x: x['datetime'], reverse=True)

    dataBase.close()
    connection.close()
    return data
