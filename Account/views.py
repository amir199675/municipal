from django.shortcuts import render , redirect , HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test


# Create your views here.



def check_staff(user):
	return user.is_staff



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

@user_passes_test(check_staff)
def Profile(request):
	select_user = request.user

	if request.method == 'POST' and 'first_name' in request.POST:
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		phone_number = request.POST['phone_number']
		national_number = request.POST['national_number']

		try:
			select_user.email = email
			select_user.phone_number = phone_number
			select_user.national_number = national_number
			select_user.first_name = first_name
			select_user.last_name = last_name
			try:
				picture = request.FILES['picture']
				select_user.picture = picture
				select_user.save()
			except:
				pass
			select_user.save()
			context = {
				'success': True,
				'infor': True,
				'message': 'مشخصات شما با موفقیت ثبت شد.',
			}
			return render(request, 'admin-panel/profile/profile.html', context)

		except:
			context = {
				'error': True,
				'infor': True,
				'message': 'مشخصات وارد شده ایراد دارد',
			}
			return render(request, 'admin-panel/profile/profile.html', context)

	if request.method == 'POST' and 'password' in request.POST:
		old_pass = request.POST['old_password']
		password = request.POST['password']
		re_password = request.POST['re_password']

		test_pass = authenticate(username=select_user.username, password=old_pass)

		if test_pass:

			if password == re_password:
				select_user.set_password(password)
				select_user.save()
				context = {
					'success': True,
					'pass_change': True,
					'message': 'تغییر رمز با موفقیت انجام شد.',

				}
				return render(request, 'admin-panel/profile/profile.html', context)
			else:
				context = {
					'error': True,
					'pass_change': True,
					'message': 'لطفا رمز جدید را با دقت وارد کنید.',
				}
				return render(request, 'admin-panel/profile/profile.html', context)
		else:
			context = {
				'error': True,
				'pass_change': True,
				'message': 'لطفا در صحیح وارد کردن رمز عبور اولیه دقت فرمایید.',

			}
			return render(request, 'admin-panel/profile/profile.html', context)
	warnings = ['برای تعویض username به ادمین سایت گزارش دهید']
	context = {
		'warnings':warnings,
		'infor':True
	}
	return render(request, 'admin-panel/profile/profile.html', context)



