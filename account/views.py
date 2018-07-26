from django.shortcuts import render

# Create your views here.
def user_login(request):
	return render(request, 'account/login.html')

def user_register(request):
	return render(request, 'account/signup.html')