from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import company, lease_tenants, manager_phone, manages
from .forms import Loginform
from django.http.response import HttpResponse
from django.db import connection, transaction

# Create your views here.
class LoginView(TemplateView):
    def login(request):
        if (request.method == "POST"):
            username=request.POST['username']
            password=request.POST['password']

            try:
                cmp = company.objects.get(user_name=username, password=password)
                request.session['username'] = username
                return redirect('data')
            except:
                return render(request, 'login.html', context=None)
            return render(request, 'login.html', context=None)
        else:
            return render(request, 'login.html', context=None)

    def create(request):
        print("REACHED", flush=True)
        if (request.method == "POST"):
            user_name=request.POST['n_username']
            password=request.POST['n_password']
            
            #get curr max user_id from table +1
            cursor = connection.cursor()
            cursor.execute("SELECT max(user_id) FROM company")
            myresult = cursor.fetchall()
            user_id = myresult[0][0]+1

            #add new user to table
            cursor.execute("INSERT INTO company(user_id,user_name,password) VALUES( %s , %s, %s)", [user_id, user_name, password])

            try:
                cmp = company.objects.get(user_name=user_name, password=password)
                request.session['username'] = user_name
                return redirect('add')
            except:
                return render(request, 'login.html', context=None)

        return render(request, 'login.html', context=None)

    def logout(request):
        try:
            del request.session['username']
        except:
            pass
        return redirect('login')
    
    def get(self, request, **kwargs):           
        return render(request, 'login.html', context=None)

# Add this view
class DataView(TemplateView):
    def get(self, request, **kwards):
        try:
            if request.session['username']!=None:
                print(request.session.items(),flush=True)
                return render(request, 'data.html', context=None)
            else:
                return redirect('loginPage')
        except:
            return redirect('loginPage')

class AddView(TemplateView):
    def get(self, request, **kwargs):
        try:
            if request.session['username']!=None:
                return render(request, 'add.html', context=None)
            else:
                return redirect('loginPage')
        except:
            return redirect('loginPage')
