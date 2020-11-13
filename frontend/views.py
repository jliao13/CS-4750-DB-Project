from django.shortcuts import render, redirect
from django.db import connection, transaction
from django.views.generic import TemplateView
from .models import company, lease_tenants, manager_phone, manages, property, manager, amenities, provides, apartment, \
    lease, apartment_parking_spots, vehicle
from django.http.response import HttpResponse
from django.db import connection, transaction
import csv, io
from django.contrib import messages


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
                    user_id = request.session['user_id']


                    cursor = connection.cursor()

                    cursor.execute("INSERT INTO lease(transaction_id,price,start_date,end_date,user_id) "
                                   "VALUES( %s , %s , %s, %s, %s)", [transaction_id, price, start_date, end_date,
                                                                     user_id])

                    cursor.execute("INSERT INTO manager(employee_id,first_name,last_name,email,user_id) "
                                   "VALUES( %s , %s , %s, %s, %s)", [employee_id, fname, lname, email,
                                                                     user_id])

                    cursor.execute("INSERT INTO lease_tenants(transaction_id,tenant_name) VALUES( %s , %s )",
                                   [transaction_id, tenants])

                    cursor.execute("INSERT INTO manager_phone(employee_id,phone_number) VALUES( %s , %s )",
                                   [employee_id, phone_number])

                    cursor.execute("INSERT INTO manages(property_id,employee_id) VALUES( %s , %s )",
                                   [pid, employee_id])

                    cursor.execute("INSERT INTO property(property_id,name,street_number,street_name,"
                                   "city,state,zip_code) VALUES( %s , %s, %s , %s , %s , %s ,%s )",
                                   [pid, p_name, street_number, street_name, city, state, zip_code])

                    cursor.execute("INSERT INTO apartment_parking_spots(property_id,parking_spot,apartment_number) "
                                   "VALUES( %s , %s , %s)", [pid, parking_spot, a_number])

                    cursor.execute("INSERT INTO provides(property_id,amenities_id) VALUES( %s , %s )",
                                   [pid, amenities_id])

                    cursor.execute("INSERT INTO amenities(amenities_id,pet_friendly,dryer_washer,ac,"
                                   "heating,internet) VALUES( %s , %s, %s , %s , %s , %s )",
                                   [amenities_id, pet, dryer, ac, heating, internet])

                    cursor.execute("INSERT INTO vehicle(license_plate,model,brand,transaction_id) "
                                   "VALUES( %s , %s , %s, %s)", [license_plate, model, brand, transaction_id])

                    cursor.execute("INSERT INTO apartment(property_id,apartment_number,style,square_feet,transaction_id) "
                                   "VALUES( %s , %s , %s, %s, %s)", [pid, a_number, style, square_feet,
                                                                     transaction_id])


                    return render(request, 'add.html', {"message": "inserted!"})
                else:
                    return render(request, 'add.html', context=None)
            else:
                return redirect('add')
        except:
            return redirect('add')

    def upload(request):
        try:
            cursor = connection.cursor()
            if request.method == "GET":
                return render(request, 'add.html', context=None)
            if request.method == "POST":
                csv_file = request.FILES['file']
                if not csv_file.name.endswith('.csv'):
                    messages.error(request, 'THIS IS NOT A CSV FILE')
                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                next(io_string)
                for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                    pid = column[0]
                    p_name = column[1]
                    street_number = column[2]
                    street_name = column[3]
                    city = column[4]
                    state = column[5]
                    zip_code = column[6]
                    employee_id = column[7]
                    fname = column[8]
                    lname = column[9]
                    email = column[10]
                    phone_number = column[11]
                    amenities_id = column[12]
                    pet = column[13]
                    dryer = column[14]
                    ac = column[15]
                    heating = column[16]
                    internet = column[17]
                    a_number = column[18]
                    style = column[19]
                    square_feet = column[20]
                    transaction_id = column[21]
                    parking_spot = column[22]
                    price = column[23]
                    start_date = column[24]
                    end_date = column[25]
                    tenants = column[26]
                    license_plate = column[27]
                    model = column[28]
                    brand = column[29]
                    user_id = request.session['user_id']

                    cursor.execute("INSERT INTO lease(transaction_id,price,start_date,end_date,user_id) "
                                   "VALUES( %s , %s , %s, %s, %s)", [transaction_id, price, start_date, end_date,
                                                                     user_id])

                    cursor.execute("INSERT INTO manager(employee_id,first_name,last_name,email,user_id) "
                                   "VALUES( %s , %s , %s, %s, %s)", [employee_id, fname, lname, email,
                                                                     user_id])

                    cursor.execute("INSERT INTO lease_tenants(transaction_id,tenant_name) VALUES( %s , %s )",
                                   [transaction_id, tenants])

                    cursor.execute("INSERT INTO manager_phone(employee_id,phone_number) VALUES( %s , %s )",
                                   [employee_id, phone_number])

                    cursor.execute("INSERT INTO manages(property_id,employee_id) VALUES( %s , %s )",
                                   [pid, employee_id])

                    cursor.execute("INSERT INTO property(property_id,name,street_number,street_name,"
                                   "city,state,zip_code) VALUES( %s , %s, %s , %s , %s , %s ,%s )",
                                   [pid, p_name, street_number, street_name, city, state, zip_code])

                    cursor.execute("INSERT INTO apartment_parking_spots(property_id,parking_spot,apartment_number) "
                                   "VALUES( %s , %s , %s)", [pid, parking_spot, a_number])

                    cursor.execute("INSERT INTO provides(property_id,amenities_id) VALUES( %s , %s )",
                                   [pid, amenities_id])

                    cursor.execute("INSERT INTO amenities(amenities_id,pet_friendly,dryer_washer,ac,"
                                   "heating,internet) VALUES( %s , %s, %s , %s , %s , %s )",
                                   [amenities_id, pet, dryer, ac, heating, internet])

                    cursor.execute("INSERT INTO vehicle(license_plate,model,brand,transaction_id) "
                                   "VALUES( %s , %s , %s, %s)", [license_plate, model, brand, transaction_id])

                    cursor.execute("INSERT INTO apartment(property_id,apartment_number,style,square_feet,transaction_id) "
                                   "VALUES( %s , %s , %s, %s, %s)", [pid, a_number, style, square_feet,
                                                                     transaction_id])
                return render(request, 'add.html', {"message": "inserted!"})
            else:
                return redirect('add')
        except:
            return redirect('add')



# class FinishRealPageView(TemplateView):
#     template_name = "finishreal.html"

# class IndexCopyPageView(TemplateView):
#     template_name = "index_copy.html"