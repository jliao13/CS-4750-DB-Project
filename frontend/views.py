from django.shortcuts import render
from django.views.generic import TemplateView
from .models import company, lease_tenants, manager_phone, manages
from .forms import Loginform

# Create your views here.
class LoginView(TemplateView):
    def get(self, request, **kwargs):
        comp = company.objects.all()
        tenants = lease_tenants.objects.all()
        m_phone = manager_phone.objects.all()
        username = ""
        # if request.method == "POST":
        #     #Get the posted form
        #     MyLoginForm = LoginForm(request.POST)
            
        #     if MyLoginForm.is_valid():
        #         username = MyLoginForm.cleaned_data['username']
        #     return render(request, 'data.html', context=None)
        # else:
        #     MyLoginForm = Loginform()
        #     return render(request, 'login.html', {"username" : username})
        request.session["LoggedIn"] = False
        print(request, flush=True)
        request.session["username"] = request.GET.get("username")
        request.session["password"] = request.GET.get("password")
        
        return render(request, 'login.html', {'comp':comp, 'tenants': tenants, 'm_phone':m_phone})
        # return render(request, 'login.html', context=None)
    # def login(self, request, **kwargs):
    #     username = 'not logged in'
    #     if request.method == 'POST':
    #         MyLoginForm = LoginForm(request.POST)

    #         if MyLoginForm.is_valid():
    #             username = MyLoginForm.cleaned_data['username']
    #             request.session['username'] = username
    #         else:
    #             MyLoginForm = LoginForm()

    #     return render(request, 'login.html', {"username" : username}})
    # def formView(request):
    #     if request.session.has_key('username'):
    #         username = request.session['username']
    #         return render(request, 'data.html', {"username" : username})
    #     else:
    #         return render(request, 'login.html', {})
    # def login(self, request):
    #     if request.method == "POST":
    #         print("running", flush=True)
    #         if (Users.objects.filter(username = request.GET.get("uname@gmail.com"), password = request.GET.get("upswd"))).exists():
    #             user = Users.objects.get(username = request.GET.get("uname@gmail.com"), password = request.GET.get("upswd"))
    #             request.session["user"] = user.id
    #             # request.session.set_expiry(10)
    #             # it shows home page
    #             return render(request,"home.html")
    #     #it shows again login page
    #     return render(request,"Login.html")

# Add this view
class DataView(TemplateView):
    template_name = "data.html"

class AddView(TemplateView):
    template_name = "add.html"

# class FinishRealPageView(TemplateView):
#     template_name = "finishreal.html"

# class IndexCopyPageView(TemplateView):
#     template_name = "index_copy.html"