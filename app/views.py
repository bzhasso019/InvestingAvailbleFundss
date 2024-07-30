from .scripts.authorisation.login import *
from .scripts.authorisation.registration import *
from .scripts.OperationsWithBalance.refill import *
from .scripts.OperationsWithBalance.withdraw import *
from .scripts.clientAdd import *
from .scripts.trading.tradeAction import *
from .scripts.trading.getTradeValue import *
from .scripts.dataProfileEdit.employeeEdit import *
from .scripts.dataProfileEdit.userEdit import *
from .scripts.deleteProfile import *
from .scripts.mainPages.manager.unlink import *
from .scripts.dataProfileEdit.employeeEdit import *
from .scripts.dataProfileEdit.userEdit import *

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render


def custom_404(request, exception):
    return render(request, '404.html', status=404)

@csrf_exempt
def registration(request):
	return registrationBack(request)


@csrf_exempt
def login(request):
	return authorisationBack(request)


@csrf_exempt
def refill(request):
	return refillBack(request)


@csrf_exempt
def withdraw(request):
	return withdrawBack(request)


@csrf_exempt
def mAddClientMail(request):
	return clientAdd(request)


@csrf_exempt
def tradeBtn(request):
	return tradeAction(request)


@csrf_exempt
def getTradeSum(request):
	return getTradeValue(request)


@csrf_exempt
def profileEditEmployee(request):
	return employeeEdit(request)


@csrf_exempt
def profileEditClient(request):
	return clientEdit(request)


@csrf_exempt
def deleteProfile(request):
	return delete_profile(request)

@csrf_exempt
def unlinkClient(request):
	return unlinkingAnAccount(request)

@csrf_exempt
def editProfile(request):
	return employeeEdit(request)

@csrf_exempt
def editProfileUser(request):
	return clientEdit(request)

@csrf_exempt
def doLogout(request):
	logout(request)
	return redirect('/auth/')
