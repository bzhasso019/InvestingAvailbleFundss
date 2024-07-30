from connection import connection_db
from app.scripts.funcs import *

def getUserData(request, uid = False, initial=False):
	# try:
		connection = connection_db()
		dataBase = connection.cursor()
		
		id = uid if uid else request.user.id
		
		dataBase.execute(f'select id_user, last_name, first_name, patronymic from auth_user where id={id}')
		data = dataBase.fetchall()[0]
		if initial:
			name = f'{data[1]} {data[2][0]}.'
			if data[3] != None:
				name += f' {data[3][0]}.'
		else:
			name = f'{data[1]} {data[2]}'
			if data[3] != None:
				name += f' {data[3]}'
		userId = id
		dataBase.execute(f'select id_employee, id_enterprise from users where id_user={data[0]}')
		data = dataBase.fetchall()[0]
		if (data[0] == None):
			dataBase.execute(f'select id_user from auth_user where id={userId}')
			idUser = dataBase.fetchall()[0][0]
			
			dataBase.execute(f'select id_portfolio from portfolios as p join users as u on p.id_enterprise=u.id_enterprise where u.id_user={idUser}')
			idPortfolio = dataBase.fetchall()[0][0]
			
			dataBase.execute(f'select total_quantity from portfolio_to_securitie where id_portfolio={idPortfolio} and id_securitie=36')
			totalQuantity = dataBase.fetchall()[0][0]
			
			dataBase.close()
			connection.close()
			return {
				'id': id,
				'name': name,
				'role': 'enterprise',
				'balance': f"{fti(totalQuantity):,.0f}".replace(',', ' ')
			}
		dataBase.execute(f'select id_post from employees where id_employee={data[0]}')
		data = dataBase.fetchall()[0][0]
		dataBase.execute(f'select post_name from posts where id_post={data}')
		role = dataBase.fetchall()[0][0]
		if role == 'Администратор':
			role = 'Admin'
		else:
			role = 'Manager'
		dataBase.close()
		connection.close()
		return {
			'id': id,
			'name': name,
			'role': role
		}
	# except:
	# 	return 'error'
	
	
	
	# return {
	# 	'name': 'Иванов Иван Иванович',
	# 	'role': 'enterprise'
	# }