from tinkoff.invest import Client, RequestError
from connection import connection_db, getTokenInvest

TOKEN = getTokenInvest()

connection = connection_db()
dataBase = connection.cursor()

dataBase.execute('select s.ticker, c.catalog_name from securities s join catalogs c on s.id_catalog = c.id_catalog;')
tickersBase = dataBase.fetchall()

tickers = {
    "Акции": [],
    "Облигации": [],
    "Фонды": [],
    "Валюта и металлы": []
}

for row in tickersBase:
    if row[0] != 'RUB':
        tickers[row[1]].append(row[0])

def getFigiByTicker(client, ticker, assetType):
    try:
        if assetType == "Акции":
            instruments = client.instruments.shares().instruments
        elif assetType == "Облигации":
            instruments = client.instruments.bonds().instruments
        elif assetType == "Фонды":
            instruments = client.instruments.etfs().instruments
        elif assetType == "Валюта и металлы":
            instruments = client.instruments.currencies().instruments
        
        for instrument in instruments:
            if instrument.ticker == ticker:
                return instrument.figi

        print(f"No FIGI found for ticker: {ticker}")
        return None
    except RequestError as e:
        print(f"Could not retrieve FIGI for {ticker}: {e}")
        return None

def getCurrentPrice(client, figi):
    try:
        response = client.market_data.get_last_prices(figi=[figi])
        if response.last_prices:
            return response.last_prices[0].price
        else:
            print(f"No price data found for FIGI {figi}")
            return None
    except RequestError as e:
        print(f"Could not retrieve price for FIGI {figi}: {e}")
        return None

with Client(TOKEN) as client:
    for asset_type, tickerList in tickers.items():
        for ticker in tickerList:
            figi = getFigiByTicker(client, ticker, asset_type)
            if figi:
                currentPrice = getCurrentPrice(client, figi)
                if currentPrice:
                    print(f"Current price for {ticker} (FIGI: {figi}): {currentPrice.units}.{str(currentPrice.nano)} RUB")
                    currentPrice = float(f'{currentPrice.units}.{str(currentPrice.nano)}')
                    dataBase.execute(f"update securities set quotation = {currentPrice} where ticker = '{ticker}'")
dataBase.execute('''with s as (select id_portfolio, sum(total_quantity * (select quotation from securities where id_securitie = p.id_securitie)) sum from portfolio_to_securitie p group by id_portfolio) update portfolios p set balance = s.sum from s where p.id_portfolio = s.id_portfolio;''')
print('Balances updated!')
connection.commit()
dataBase.close()
connection.close()