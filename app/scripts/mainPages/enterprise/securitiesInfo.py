from connection import connection_db
from app.scripts.funcs import fti


def securitiesInfo(securities):
    connection = connection_db()
    dataBase = connection.cursor()
    
    info = {
        'stocks_data': [],
        'bonds_data': [],
        'funds_data': [],
        'curr_metals_data': []
    }
    
    infoIndices = {
        1: 'stocks_data',
        2: 'bonds_data',
        3: 'funds_data',
        4: 'curr_metals_data',
    }

    for securitie in securities:
        idSecuritie = securitie[1]
        totalQuantity = securitie[2]

        dataBase.execute(f'select id_catalog, sec_name, ticker, quotation, icon from securities where id_securitie={idSecuritie}')
        idCatalog, securitieName, ticker, currentQuotation, iconPath = dataBase.fetchall()[0]

        if ticker != 'RUB':
            currentTotalPrice = currentQuotation * totalQuantity

            dataBase.execute(f'select quantity, total_price from requests where id_securitie={idSecuritie}')
            data = dataBase.fetchall()[0]
            oldQuantity = data[0]
            oldTotalPrice = data[1]
            oldQuotation = oldTotalPrice / oldQuantity
            securitieInfo = {
                'name': securitieName,
                'short_name': ticker,
                'img': iconPath,
                'price_buy': fti(oldQuotation),
                'price_now': fti(currentQuotation),
                'price_count_buy': fti(currentTotalPrice),
                'count_buy': fti(totalQuantity),
                'price_end': fti((currentQuotation - oldQuotation) * totalQuantity),
                'proc_end': fti((float(currentQuotation) / float(oldQuotation) - 1) * 100)
            }
            info[infoIndices[idCatalog]].append(securitieInfo)

    return info