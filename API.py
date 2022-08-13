import requests

def Login(User, Password):
	session = requests.Session()
	response1 = session.get('https://www.faaflightschools.com/')
	data = {
		'kt_login_user': User,
		'kt_login_password': Password,
		'kt_login1': 'Login'
	}
	response = session.post('https://www.faaflightschools.com/login.php', data=data)
	return response1.cookies.get_dict()
