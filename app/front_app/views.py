from django.shortcuts import render
from django.http import HttpResponseRedirect

from .viewBack.getUserData import getUserData
from .viewBack.getColorImg import getColorImg

from app.scripts.analytics.short.shortAnalyticsBalance import shortAnalyticsBalance
from app.scripts.analytics.short.shortAnalyticsBar import shortAnalyticsBar
from app.scripts.analytics.short.shortAnalyticsPie import shortAnalyticsPie
from app.scripts.analytics.all.getAnalyticsPie import analyticsPie

from app.scripts.clientProfile import private_profile
from app.scripts.managerProfile import manager_profile
from app.scripts.OperationsWithBalance.operationsHistory import history
from app.scripts.mainPages.enterprise.enterpriseMainPage import enterpriseMainPage

#manager
from app.scripts.mainPages.manager.managerMainPage import managerMainPage
from app.scripts.OperationsWithBalance.operationsHistoryManager import historyManager
from app.scripts.trading.getSecuritiesByCatalog import getSecuritiesByCatalog
from app.scripts.trading.getSecuritieInfo import getSecuritieInfo
from app.scripts.trading.tradingHistory import trading_history

#admin
from app.scripts.mainPages.admin.adminMainPage import adminMainPage

def nav(data):
    href = '/'
    val = "<a href='/' class='col_bvio'>Главная страница</a> / "

    for item in data:
        if len(item) == 2:
            href += f'{item[0]}/'
            val += f"<a href='{href}' class='col_bvio'>{item[1]}</a> / "
        else:
            val += f"<a href='/{item[0]}' class='col_bvio'>{item[1]}</a> / "

    return val

def chAuth(request):
    if request.user.id == None:
        return HttpResponseRedirect("/auth/")
    return None

def ret(request, url, data = {}):
    if url == 'auth.html':
        return HttpResponseRedirect("/auth/")
    chAuth(request)
    return render(request, url, data)
    
def toOops():
        return HttpResponseRedirect("/oops/")

def viewOops(request):
        return render(request, 'oops.html')

def viewAuth(request):
    if request.user.id == None:
        return render(request, 'auth.html')
    else:
        return HttpResponseRedirect("/")


def viewRegistration(request):
    if request.user.id == None:
        return render(request, 'registration.html')
    else:
        userData = getUserData(request)
        if userData['role'] != 'Admin':
            return HttpResponseRedirect("/")
        else:
            return render(request, 'registration.html', {'userData': userData})


def viewHome(request):
    if chAuth(request) != None:
        return chAuth(request)
    
    userData = getUserData(request)

    if userData['role'] == 'enterprise':
        aBal, aProc = shortAnalyticsBalance(request)
        aBarMonth, aBarCount, aBarSum = shortAnalyticsBar(request)
        aPie = shortAnalyticsPie(request)
        balanceData, secData, entName = enterpriseMainPage(request)
        data = {
            'userData': userData,
            'nav': nav([]),
            'in_scripts_graph': True,
            
            'balance': balanceData['balance'],
            'var_balance': balanceData['var_balance'],
            'var_balance_proc': balanceData['balance_proc'],
            'var_balance_1': aBal,
            'var_balance_proc_1': aProc,
            'graph_bar': {
                'month': aBarMonth,
                'count': aBarCount,
                'sum': aBarSum
            },
            'graph_pie': aPie,
            'stocks_data': secData['stocks_data'],
            'bonds_data': secData['bonds_data'],
            'funds_data': secData['funds_data'],
            'curr_metals_data': secData['curr_metals_data']
        }
        return ret(request, 'index.html', data)
    elif userData['role'] == 'Manager':
        data = {
            'userData': userData,
            'nav': nav([]),
            'users': managerMainPage(request)
        }
        return ret(request, 'Mindex.html', data)
    elif userData['role'] == 'Admin':
        data = {
            'userData': userData,
            'nav': nav([]),
            'users': adminMainPage()
        }
        return ret(request, 'Aindex.html', data)
    else:
        return ret(request, 'auth.html')



def viewProfile(request, id=None):
    if chAuth(request) != None:
        return chAuth(request)
    
    edit = request.GET.get('edit')
    
    userData = getUserData(request)
    userData1 = getUserData(request, id, True)

    dataProfile = []
    if userData['role'] == 'enterprise' or userData1['role'] == 'enterprise':
        dataProfile = private_profile(request, id)
    else:
        dataProfile = manager_profile(request, id)
    data = {
        'userData': userData,
        'nav': nav([['profile', 'профиль']]),
        'userData1': userData1,
        'edit': edit,
        'data': dataProfile
    }
    return ret(request, 'profile.html', data)


def viewPayment(request):
    if chAuth(request) != None:
        return chAuth(request)
    
    data = {
        'userData': getUserData(request),
        'nav': nav([['payment', 'пополнение']]),
    }
    return ret(request, 'payment.html', data)
    

def viewWithdraw(request):
    if chAuth(request) != None:
        return chAuth(request)
    
    userData = getUserData(request)
    
    data = {
        'userData': userData,
        'nav': nav([['withdraw', 'вывод']])
    }
    return ret(request, 'withdraw.html', data)


def viewOperations(request):
    if chAuth(request) != None:
        return chAuth(request)
    
    userData = getUserData(request)
    data = history(request)[1] if userData['role'] == 'enterprise' else historyManager(request)
    if userData['role'] in ['enterprise', 'Manager', 'Admin']:
        data = {
            'userData': userData,
            'nav': nav([['operations', 'история операций']]),
            'bodyClass': 'operations_list' if userData['role'] in ['Manager', 'Admin'] else '',
            'operations_data': data
        }
        return ret(request, 'operations.html', data)
    else:
        return ret(request, 'auth.html')
    
def viewOperationsDetail(request, id):
    if chAuth(request) != None:
        return chAuth(request)
    
    userData = getUserData(request)
    name, dataHistory = history(request, id)
    # if data == 'Error':
    #     return toOops()
    
    if userData['role'] == 'Manager':
        userData = getUserData(request)
        name, dataHistory = history(request, id)
        # if data == 'Error':
        #     return toOops()
        data = {
            'userData': userData,
            'nav': nav([[f'enterprise/{id}', f'клиент <b>{name}</b>', ''], [f'operations/{id}', 'история операций']]),
            'name': name,
            'operations_data': dataHistory
        }
        return ret(request, 'MoperationsDetail.html', data)
    elif userData['role'] == 'Admin':
        userData = getUserData(request, id)
        if userData['role'] == 'Manager':
            dataHistory = historyManager(request, id)
            data = {
                'userData': userData,
                'nav': nav([[f'enterprise/{id}', f'клиент <b>{name}</b>', ''], [f'operations/{id}', 'история операций']]),
                'name': name,
                'operations_data': dataHistory
            }
        else:
            name, dataHistory = history(request, id)
            data = {
                'userData': userData,
                'nav': nav([[f'enterprise/{id}', f'клиент <b>{name}</b>', ''], [f'operations/{id}', 'история операций']]),
                'name': name,
                'operations_data': dataHistory
            }

        return ret(request, 'operations.html', data)
    else:
        return ret(request, 'auth.html')


def viewAnalytic(request, id=None):
    if chAuth(request) != None:
        return chAuth(request)
    
    userData = getUserData(request)
    datas = analyticsPie(request, id)
    
    if datas != 'Error':
        for key in datas[0].keys():
            if datas[0][key] != []:
                if datas[0][key][0]['img'] != 'None':

                    icos = getColorImg([obj['img'] for obj in datas[1][key]])
                    for obj, col in zip(datas[0][key], icos):
                        obj['color'] = col

    if userData['role'] == 'enterprise':
        nav1 = [['analytic', 'аналитика']]
    if userData['role'] in ['Manager', 'Admin']:
        nav1 = [[f'enterprise/{id}', f'клиент', ''], [f'analytic/{id}', 'аналитика']]

    data = {
        'userData': userData,
        'nav': nav(nav1),
        'in_scripts_graph': True,
        'in_slick': True,
        
        'pie': datas[0],
        'securities': datas[1],
    }
    return ret(request, 'analytic.html', data)
    

#Manager
def viewEnterprise(request, id):
    if chAuth(request) != None:
        return chAuth(request)
    
    userData = getUserData(request)

    if userData['role'] in ['Manager', 'Admin']:
        aBal, aProc = shortAnalyticsBalance(request, id)
        aBarMonth, aBarCount, aBarSum = shortAnalyticsBar(request, id)
        aPie = shortAnalyticsPie(request, id)
        balanceData, secData, entName = enterpriseMainPage(request, id)

        if 'Error' in [aBal, aPie, aBarMonth, balanceData]:
            return toOops()

        data = {
            'userData': userData,
            'id': id,
            'nav': nav([[f'enterprise/{id}', f'клиент <b>{entName}</b>']]),
            'in_scripts_graph': True,
                        
            'enterprise_name': entName,
            'balance': balanceData['balance'],
            'var_balance': balanceData['var_balance'],
            'var_balance_proc': balanceData['balance_proc'],
            'var_balance_1': aBal,
            'var_balance_proc_1': aProc,
            'graph_bar': {
                'month': aBarMonth,
                'count': aBarCount,
                'sum': aBarSum
            },
            'graph_pie': aPie,
            'stocks_data': secData['stocks_data'],
            'bonds_data': secData['bonds_data'],
            'funds_data': secData['funds_data'],
            'curr_metals_data': secData['curr_metals_data']
        }
        return ret(request, 'index.html', data)
    else:
        return ret(request, 'auth.html')

def viewTradeHistory(request, id):
    if chAuth(request) != None:
        return chAuth(request)
    
    userData = getUserData(request)

    if userData['role'] in ['Manager', 'Admin']:
        tradeData = trading_history(id)
        data = {
            'userData': userData,
            'id': id,
            'nav': nav([[f'enterprise/{id}', 'клиент', ''], [f'tradeHistory/{id}', 'история торговли']]),
            'sec_data': tradeData
        }
        return ret(request, 'tradeHistory.html', data)
    else:
        return ret(request, 'auth.html')


def viewTrade(request, id):
    if chAuth(request) != None:
        return chAuth(request)
    
    userData = getUserData(request)
    type = request.GET.get('type')
    securities = getSecuritiesByCatalog(request, id)

    if userData['role'] in ['Manager', 'Admin']:
        data = {
            'userData': userData,
            'nav': nav([[f'enterprise/{id}', 'клиент', ''], [f'trade/{id}', f'торговля']]),
            'type': type,
            'stocks_data': securities['stocks_data'],
            'bonds_data': securities['bonds_data'],
            'funds_data': securities['funds_data'],
            'curr_metals_data': securities['curr_metals_data']
        }
        return ret(request, 'trade.html', data)
    else:
        return ret(request, 'auth.html')


def viewSecuritiesTrade(request, id, ticker):
    if chAuth(request) != None:
        return chAuth(request)
    
    userData = getUserData(request)
    securities = getSecuritieInfo(request, id, ticker)

    if userData['role'] in ['Manager', 'Admin']:
        name = securities['security_name']
        type = securities['type']
        data = {
            'userData': userData,
            'id': id,
            'type': type,
            'nav': nav([[f'enterprise/{id}', 'клиент', ''], [f"trade/{id}/?type={type['eng']}", type['href_rus'], ''], [f'securitiesTrade/{id}/{ticker}', name]]),
            'in_scripts_graph': True,

            'security': securities
        }
        return ret(request, 'securitiesTrade.html', data)
    else:
        return ret(request, 'auth.html')


#admin
def viewEmployee(request, id):
    if chAuth(request) != None:
        return chAuth(request)
    
    userData = getUserData(request)
    
    if userData['role'] == 'Admin':
        data = {
            'userData': userData,
            'nav': nav([[f'employee/{id}', 'Сотрудник', '']]),
            'id': id,
            'userData1': getUserData(request, id, True),
            'users': managerMainPage(request, id)
        }
        return ret(request, 'Mindex.html', data)
    else:
        return ret(request, 'auth.html')