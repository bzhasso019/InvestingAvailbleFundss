from django.http import HttpResponse
from re import findall, sub
from json import dumps
from datetime import datetime as dt

fti = lambda f: float(str(round(f, 2))) if f != int(f) else int(f)

def check(string, param):
	patterns = {
		'mail': r'\b[\w\d]+@\w+\.\w+\b'
	}
	return findall(patterns[param], string) == []

def numFormat(num):
	return sub(r'\B(?=(\d{3})+(?!\d))', ' ', str(num))

def insertSql(table, params):
	return f'''insert into {table}
values
(default, \'''' + '\', \''.join(params) + '\')'

def getId(cursor, table, idColumn):
	cursor.execute(f'select {idColumn} from {table}')
	result = cursor.fetchall()
	return result[-1][0]

def checkPass(password):
	availableSymbols = [i for i in range(48, 58)]
	availableSymbols.extend([i for i in range(97, 123)])
	return list(filter(lambda g: not(ord(g) in availableSymbols), list(password.lower()))) != []

def returnJson(data={}, status='', message=''):
	if data == {}:
		data2 = {
			'status': status,
			'message': message
		}
	else:
		data2 = data
	return HttpResponse(dumps(data2, ensure_ascii=False), content_type='application/json')

def cardValidation(amount, cardNumber, cardDate = ''):
	errorsDict = {}
	
	if amount <= 0:
		errorsDict['amount'] = 'Некорректная сумма перевода'
	
	if len(cardNumber) != 16:
		errorsDict['card_number'] = 'Некорректный номер карты'
	
	if cardDate != '':
		cardDateFlag = False
		if len(cardDate) == 2:
			if int(cardDate[0]) in [i for i in range(1,13)]:
				cardDate = dt.strptime(f'20{cardDate[1]}/{cardDate[0]}/01', '%Y/%m/%d')
				if cardDate < dt.today():
					cardDateFlag = True
			else:
				cardDateFlag = True
		else:
			cardDateFlag = True
		
		if cardDateFlag:
			errorsDict['card_date'] = 'Карта недействительна или некорректный срок действия карты'
	
	return errorsDict
		