from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from app.scripts.funcs import returnJson

def authorisationBack(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		return returnJson(status='success')
	return returnJson(status='Error', message='Неверный логин или пароль')