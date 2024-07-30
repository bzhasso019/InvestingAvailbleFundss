from connection import connection_db
from app.scripts.funcs import fti


def getPortfolioData(portfolio):
    balance = portfolio[1]
    deposition = portfolio[3]
    uid, initials = getInitials(portfolio[5])
    balanceChange = 0
    if deposition:
        balanceChange = fti((float(balance) / float(deposition) - 1) * 100)
    portfolioInfo = {
        'id': uid,
        'name': initials,
        'balance': fti(balance),
        'balance_proc': fti(balanceChange),
    }
    return portfolioInfo

def getInitials(id_enterprise):
    connection = connection_db()
    dataBase = connection.cursor()

    dataBase.execute(f'select id_user from Users where id_enterprise={id_enterprise}')
    id_user = dataBase.fetchall()[0][0]

    dataBase.execute(f'select id, last_name, first_name, patronymic from auth_user where id_user={id_user}')
    data = dataBase.fetchall()[0]
    id = data[0]
    clientLastName = data[1]
    clientFirstName = data[2]
    clientPatronymic = data[3]

    initials = f'{clientLastName} {clientFirstName[0]}.'
    if clientPatronymic != None:
        initials += f' {clientPatronymic[0]}.'
    connection.commit()
    dataBase.close()
    connection.close()
    return [id, initials]