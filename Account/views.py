from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def Login (request):
	if request.method == 'POST' and 'username' in request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active :
				login(request, user)
				if 'next' in request.POST:
					return redirect(request.POST['next'])
				return redirect('Site_Panel:deceased_list')
		else:
			context = {
				'error':True,
				'message':'اطلاعات وارد شده صحیح نیست.'
					   }
			return render(request, 'admin-panel/login/login.html', context)
	context = {}
	return render(request,'admin-panel/login/login.html',context)