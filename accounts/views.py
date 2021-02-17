from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
# Create your views here.
def login(request):
    if request.method == 'POST':
        #musername = request.POST.get('username')
        musername = request.POST['username']
        print(musername)
        #password = request.POST.get('password')
        password = request.POST['password']
        print(password)
        user = auth.authenticate(username=musername , password=password)
        print("user is",user)

        if user is  None:
            print('Username or Password not matched')
            return redirect('login')
        else:
            auth.login(request,user)
            print("created")
            return redirect('/')
    else:
        return render(request,'accounts/login.html')
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
           if User.objects.filter(username=username).exists():
               messages.info(request,'Username Taken')
               return redirect('register')
           elif User.objects.filter(email=email).exists():
               messages.info(request, 'Email Taken')
               return redirect('register')
           else:
               user = User.objects.create_user(username=username,password=password1,email=email, first_name=first_name,last_name=last_name)
               user.save()
               return redirect('login')
        else:
            print("Password not matching")
            return redirect('register')

    else:
        return render(request,'accounts/index.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def profile(req):
    return render(req,'profile_page.html')
