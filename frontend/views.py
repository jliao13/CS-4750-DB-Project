from django.shortcuts import render
from django.db import connection, transaction
from django.views.generic import TemplateView
from .models import company, lease_tenants, manager_phone, manages, property, manager, amenities, provides, apartment, \
    lease, apartment_parking_spots, vehicle
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
        spots = apartment_parking_spots.objects.all()
        vehicles = vehicle.objects.all()

        return render(request, 'data.html', {'comp': comp, 'tenants': tenants, 'm_phone': m_phone, 'properties':
            properties, 'managers': managers, 'manage_props': manage_props, 'amenities': ameneties_list, 'provides':
            provides_amenities, 'apartments': apartments, 'leases': leases, 'parking_spots': spots, 'vehicles': vehicles})

class AddView(TemplateView):
    template_name = "add.html"

    def add(request):
        if(request.method == "POST"):
            cursor = connection.cursor()
            pid = request.POST.get("property-id")
            p_name = request.POST.get("property-name")
            street_number = request.POST.get("street-number")
            street_name = request.POST.get("street-name")
            city = request.POST.get("city")
            state = request.POST.get("state")
            zip_code = request.POST.get("zip-code")
            employee_id = request.POST.get("employee-id")
            fname = request.POST.get("fname")
            lname = request.POST.get("lname")
            email = request.POST.get("email")
            phone_number = request.POST.get("phone-number")
            amenities_id = request.POST.get("amenities-id")
            pet = request.POST.get("pet-friendly")
            dryer = request.POST.get("dryer-washer")
            ac = request.POST.get("ac")
            heating = request.POST.get("heating")
            internet = request.POST.get("internet")
            a_number = request.POST.get("apartment-number")
            style = request.POST.get("style")
            square_feet = request.POST.get("square-feet")
            transaction_id = request.POST.get("transaction-id")
            parking_spot = request.POST.get("parking-spot")
            price = request.POST.get("price")
            start_date = request.POST.get("start-date")
            end_date = request.POST.get("end-date")
            tenants = request.POST.get("tenant-name")
            license_plate = request.POST.get("license-plate")
            model = request.POST.get("model")
            brand = request.POST.get("brand")

            table1 = lease_tenants(transaction_id=transaction_id, tenant_name=tenants)
            table1.save()

            table2 = manager_phone(employee_id=employee_id, phone_number=phone_number)
            table2.save()

            table3 = manages(property_id=pid, employee_id=employee_id)
            table3.save()

            table4 = property(property_id=pid, name=p_name, street_number=street_number,
                              street_name=street_name, city=city, state=state, zip_code=zip_code)
            table4.save()

            table6 = apartment_parking_spots(property_id=pid, parking_spot=parking_spot, apartment_number=a_number)
            table6.save()

            table7 = provides(property_id=pid, amenities_id=amenities_id)
            table7.save()

            table8 = amenities(amenities_id=amenities_id, pet_friendly=pet, dryer_washer=dryer,
                                ac=ac, heating=heating, internet=internet)
            table8.save()

            table9 = vehicle(license_plate=license_plate, model=model, brand=brand,
                             transaction_id=transaction_id)
            table9.save()

            table10 = lease(transaction_id=transaction_id, price=price, start_date=start_date,
                            end_date=end_date, user_id=1)
            table10.save()

            table11 = manager(employee_id=employee_id, first_name=fname, last_name=lname,
                              email=email, user_id=1)
            table11.save()

            table12 = apartment(property_id=pid, apartment_number=a_number, style=style,
                                square_feet=square_feet, transaction_id=transaction_id)
            table12.save()


        return render(request, 'add.html', {"message": "inserted!"})


# class FinishRealPageView(TemplateView):
#     template_name = "finishreal.html"

# class IndexCopyPageView(TemplateView):
#     template_name = "index_copy.html"