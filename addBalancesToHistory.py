from .connection import connection_db

connection = connection_db()
dataBase = connection.cursor()
dataBase.execute('select id_portfolio, balance from portfolios')
result = dataBase.fetchall()
for row in result:
	dataBase.execute(f'insert into balances_history values ({row[0]}, now(), {row[1]})')
connection.commit()
dataBase.close()
connection.close()