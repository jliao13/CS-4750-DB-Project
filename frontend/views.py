from django.shortcuts import render
from django.views.generic import TemplateView
from .models import company, lease_tenants, manager_phone, manages, property, manager, amenities, provides, apartment,lease
# Create your views here.
class LoginView(TemplateView):
    def get(self, request, **kwargs):
        comp = company.objects.all()
        tenants = lease_tenants.objects.all()
        m_phone = manager_phone.objects.all()
        
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

# Add this view
class DataView(TemplateView):
    template_name = "data.html"

    def get(self, request, **kwargs):
        comp = company.objects.all()
        tenants = lease_tenants.objects.all()
        m_phone = manager_phone.objects.all()
        properties = property.objects.all()
        managers = manager.objects.all()
        manage_props = manages.objects.all()
        ameneties_list = amenities.objects.all()
        provides_amenities = provides.objects.all()
        apartments = apartment.objects.all()
        leases = lease.objects.all()

        return render(request, 'data.html', {'comp': comp, 'tenants': tenants, 'm_phone': m_phone, 'properties':
            properties, 'managers': managers, 'manage_props': manage_props, 'amenities': ameneties_list, 'provides':
            provides_amenities, 'apartments': apartments, 'leases': leases})

class AddView(TemplateView):
    template_name = "add.html"

# class FinishRealPageView(TemplateView):
#     template_name = "finishreal.html"

# class IndexCopyPageView(TemplateView):
#     template_name = "index_copy.html"