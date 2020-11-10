from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import company, lease_tenants, manager_phone, manages
from .forms import Loginform
from django.http.response import HttpResponse

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

    def logout(request):
        try:
            del request.session['username']
        except:
            pass
        return render(request, 'login.html', context=None)
    
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
