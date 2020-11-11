from django.shortcuts import render, redirect
from django.db import connection, transaction
from django.views.generic import TemplateView
from .models import company, lease_tenants, manager_phone, manages, property, manager, amenities, provides, apartment, \
    lease, apartment_parking_spots, vehicle
from django.http.response import HttpResponse
from django.db import connection, transaction

# Create your views here.
class LoginView(TemplateView):
    def login(request):
        if (request.method == "POST"):
            username=request.POST['username']
            password=request.POST['password']

            try:
                #check username and password and get user_id
                cursor = connection.cursor()
                cursor.execute("SELECT user_id FROM company WHERE user_name=%s AND password=%s", [username, password])
                myresults = cursor.fetchall()
                request.session['username'] = username
                request.session['user_id'] = myresults[0][0]
                return redirect('data')
            except:
                return render(request, 'login.html', context=None)
            return render(request, 'login.html', context=None)
        else:
            return render(request, 'login.html', context=None)

    def create(request):
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
                cursor = connection.cursor()
                cursor.execute("SELECT user_id FROM company WHERE user_name=%s AND password=%s", [user_name, password])
                myresults = cursor.fetchall()
                request.session['username'] = user_name
                request.session['user_id'] = myresults[0][0]
                request.session['username'] = user_name
                print(request.session['user_id'], flush=True)
                return redirect('add')
            except:
                return render(request, 'login.html', context=None)

        return render(request, 'login.html', context=None)

    def logout(request):
        try:
            del request.session['username']
            del request.session['user_id']
        except:
            pass
        return redirect('login')
    
    def get(self, request, **kwargs):           
        return render(request, 'login.html', context=None)

# Add this view
class DataView(TemplateView):

    def get(self, request, **kwargs):
        try:
            if request.session['username']!=None:
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
            else:
                return redirect('loginPage')
        except:
            return redirect('loginPage')

    
    def delete(request, property_id, apartment_number):
        apartment.objects.filter(property_id=property_id, apartment_number=apartment_number).delete()
        return redirect("/../data")

    def update(request):
        if request.method == "POST":
            transaction_id = request.POST.get("transaction-id")
            tenants = request.POST.get("tenant-name")

            table1 = lease_tenants(transaction_id=transaction_id, tenant_name=tenants)
            table1.save()
        return redirect("/../data")


class AddView(TemplateView):

    def get(self, request, **kwargs):
        try:
            if request.session['username']!=None:
                return render(request, 'add.html', context=None)
            else:
                return redirect('loginPage')
        except:
            return redirect('loginPage')

    def add(request):
        try:
            if request.session['username']!=None:
                if request.method == "POST":
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
                else:
                    return render(request, 'add.html', context=None)
            else:
                return redirect('loginPage')
        except:
            return redirect('loginPage')


# class FinishRealPageView(TemplateView):
#     template_name = "finishreal.html"

# class IndexCopyPageView(TemplateView):
#     template_name = "index_copy.html"