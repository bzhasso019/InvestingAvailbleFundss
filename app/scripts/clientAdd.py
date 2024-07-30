from connection import connection_db
from app.scripts.funcs import returnJson
from app.scripts.mainPages.manager.managerMainModule import getPortfolioData

def clientAdd(request):
	connection = connection_db()
	dataBase = connection.cursor()
	
	username = request.POST.get('email')
	id = request.POST.get('id')
	
	idE = id if id else request.user.id
	
	dataBase.execute(f'select id_user from auth_user where username=\'{username}\'')
	idUserEnt = dataBase.fetchall()
	if idUserEnt == []:
		return returnJson(status='error', message='Такого пользователя не существует')
	idUserEnt = idUserEnt[0][0]
	dataBase.execute(f'select id_enterprise from users where id_user={idUserEnt}')
	idEnterprise = dataBase.fetchall()[0][0]
	if idEnterprise == None:
		return returnJson(status='error', message='Такого клиента не существует')
	
	dataBase.execute(f'select id_user from auth_user where id={idE}')
	idUserEmp = dataBase.fetchall()[0][0]
	dataBase.execute(f'select id_employee from users where id_user={idUserEmp}')
	idEmployee = dataBase.fetchall()[0][0]
	
	dataBase.execute(f'select id_employee from portfolios where id_enterprise={idEnterprise}')
	idEmployeePortfolio = dataBase.fetchall()[0][0]
	if idEmployeePortfolio != None:
		if idEmployeePortfolio == idEmployee:
			return returnJson(status='error', message='Клиент уже работает с вами')
		return returnJson(status='error', message='Клиент уже работает с другим менеджером')
	
	dataBase.execute(f'update portfolios set id_employee={idEmployee} where id_enterprise={idEnterprise}')
	
	dataBase.execute(f'select * from portfolios where id_enterprise={idEnterprise}')
	portfolio = getPortfolioData(dataBase.fetchall()[0])
	portfolio['status'] = 'success'
	portfolio['message'] = 'Клиент добавлен'
	
	connection.commit()
	dataBase.close()
	connection.close()
	return returnJson(data=portfolio)