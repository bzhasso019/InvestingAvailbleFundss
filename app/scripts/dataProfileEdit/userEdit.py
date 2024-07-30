from connection import *
from app.scripts.funcs import *


def clientEdit(request):
    email = request.POST.get('email')
    name = request.POST.get('name')
    phone = request.POST.get('phone').replace('+7', '8')
    address = request.POST.get('address')
    typeProperty = request.POST.get('type_property')
    title = request.POST.get('title')
    idUser = request.POST.get('id')
    
    connection = connection_db()
    dataBase = connection.cursor()
    
    idUser = idUser if idUser else request.user.id

    errorsDict = {}

    if len(email) > 150:
        errorsDict['email'] = 'Почта слишком длинная'

    if len(address) > 150:
        errorsDict['address'] = 'Адрес слишком длинный'

    if len(typeProperty) > 100:
        errorsDict['typeProperty'] = 'Вид собственности слишком длинный'

    if len(title) > 50:
        errorsDict['title'] = 'Наименование организации слишком длинное'

    if check(email, 'mail'):
        errorsDict['email'] = 'Введите корректную почту'
    
    dataBase.execute(f'select email from auth_user where id!={idUser}')
    if dataBase.fetchall() != []:
        errorsDict['email'] = 'Данная почта уже используется'
    
    dataBase.execute(f'select id_user from auth_user where id={idUser}')
    idUserUsers = dataBase.fetchall()[0][0]
    
    dataBase.execute(f"select id_enterprise from Users where id_user={idUserUsers}")
    idEnterprise = dataBase.fetchall()[0][0]
    
    if not (len(phone) == 11 and phone.isdigit()):
        errorsDict['phone'] = 'Телефон введён некорректно'
    
    dataBase.execute(f'select tel from enterprises where id_enterprise={idEnterprise}')
    if dataBase.fetchall() != []:
        errorsDict['phone'] = 'Данный номер телефона уже используется'

    splitName = name.split()

    if len(splitName) < 2:
        errorsDict['name'] = 'ФИО введён некорректно'
    else:

        lastName, firstName, *args = splitName

        lastName = lastName.capitalize()
        firstName = firstName.capitalize()
        patronymic = "Null"

        if args != []:
            patronymic = f"'{args[0].capitalize()}'"

        if len(firstName) > 150 or len(lastName) > 150 or len(patronymic) > 150:
            errorsDict['name'] = 'ФИО слишком длинное'

    if errorsDict != {}:
        return returnJson(data=errorsDict)

    dataBase.execute(f"update auth_user set email='{email}' where id={idUser}")
    
    dataBase.execute(f"update auth_user set first_name='{firstName}', last_name='{lastName}', patronymic={patronymic} where id={idUser}")

    dataBase.execute(f"update enterprises update set tel='{phone}', address='{address}', type_property='{typeProperty}', title='{title}' where id_enterprise={idEnterprise}")
    
    connection.commit()
    dataBase.close()
    connection.close()
    return returnJson(status='success', message='Данные обновлены')
