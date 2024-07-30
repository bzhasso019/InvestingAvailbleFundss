from connection import connection_db
from app.scripts.funcs import returnJson

def unlinkingAnAccount(request):

    uid = request.POST.get('uid')

    connection = connection_db()
    dataBase = connection.cursor()

    dataBase.execute(f"select id_user from auth_user where id='{uid}'")
    id_user_client = dataBase.fetchall()[0][0] 

    dataBase.execute(f"select id_enterprise from Users where id_user='{id_user_client}'")
    id_enterprise = dataBase.fetchall()[0][0]
    
    dataBase.execute(f"update portfolios set id_employee = null where id_enterprise={id_enterprise}")

    connection.commit()
    dataBase.close()
    connection.close()
    return returnJson(status='success', message='Аккаунт отвязан успешно')
