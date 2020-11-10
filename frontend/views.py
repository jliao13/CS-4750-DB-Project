from django.shortcuts import render
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
                authenticated = True
                # return redirect(AddView, authenticated= )
                return render(request, 'data.html', {"company": cmp, "authenticated": authenticated})
            except:
                return render(request, 'login.html', context=None)
            return render(request, 'login.html', context=None)
        else:
            return render(request, 'login.html', context=None)
    
    def get(self, request, **kwargs):              
        return render(request, 'login.html', context=None)

# Add this view
class DataView(TemplateView):
    def get(self, request, **kwards):
        return render(request, 'data.html', context=None)

class AddView(TemplateView):
    def get(self, request, **kwards):
        return render(request, 'add.html', context=None)
