from connection import connection_db
from app.scripts.funcs import returnJson, fti, numFormat


def getTradeValue(request):
    ticker = request.POST.get('ticker')
    quantity = int(request.POST.get('quantity'))
    
    connection = connection_db()
    dataBase = connection.cursor()
    
    dataBase.execute(f'select quotation from securities where ticker = \'{ticker}\'')
    cost = dataBase.fetchall()[0][0]
    
    cost *= quantity
    cost = numFormat(fti(cost))
    
    return returnJson(status = 'success', message = f'{cost} ₽')