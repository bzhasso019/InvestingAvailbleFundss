from connection import connection_db

def manager_profile(request, id=None):
    try:
        id = id if id != None else request.user.id

        connection = connection_db()
        dataBase = connection.cursor()

        dataBase.execute(f"select last_name, first_name, patronymic, email from auth_user where id={id}")
        data = dataBase.fetchall()[0]

        lastName = data[0]
        firstName = data[1]
        patronymic = data[2]
        email = data[3]

        name = f'{lastName} {firstName}'
        if patronymic != None:
            name += f' {patronymic}'
            
        data = {
            'email': email,
            'name': name,
        }

        dataBase.close()
        connection.close()
        return data
    except:
        return 'Error'