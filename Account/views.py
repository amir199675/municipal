from django.shortcuts import render , redirect , HttpResponse
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def Login (request):
	if request.user.is_authenticated and request.user.is_staff:
		return redirect('Site_Panel:index')

	if request.method == 'POST' and 'username' in request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active :
				login(request, user)
				url = request.get_full_path()
				url = url.replace('logout','login')
				if 'next' in url:
					next = url.split('/Account/login/?next=')
					return redirect(next[1])
				return redirect('Site_Panel:index')
		else:
			context = {
				'error':True,
				'message':'اطلاعات وارد شده صحیح نیست.'
					   }
			return render(request, 'admin-panel/login/login.html', context)
	else:
		context = {}
		return render(request,'admin-panel/login/login.html',context)

def Logout(request):
	if 'next' in request.get_full_path():
		next = request.get_full_path().split('/Account/logout/?next=')
		logout(request)
		return redirect(next[1])
	logout(request)

