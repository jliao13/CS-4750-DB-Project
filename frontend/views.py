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

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]

def create_general_table(properties, apartments, manage_props, managers, provides_amenities, amenities_list, leases):
    # property apartment manage_props managers provides
    # amenities lease
    table = []
    for prop in properties:
        row= {}
        for apt in apartments:
            if prop['property_id'] == apt['property_id']:
                for mp in manage_props:
                    if mp['property_id'] == prop['property_id']:
                        for man in managers:
                            if int(man['employee_id']) == mp['employee_id']:
                                row['property_id'] = prop['property_id']
                                row['name'] = prop['name']
                                row['employee_id'] = man['employee_id']
                                row['first_name'] = man['first_name']
                                row['last_name'] = man['last_name']
                                row['email'] = man['email']
                for prov in provides_amenities:
                    if prov['property_id'] == prop['property_id']:
                        for am in amenities_list:
                            if prov['amenities_id'] == am['amenities_id']:
                                row['amenities_id'] = am['amenities_id']
                row['apartment_number'] = apt['apartment_number']
                row['style'] = apt['style']
                for l in leases:
                    if l['transaction_id'] == apt['transaction_id']:
                        row['square_feet'] = apt[
                            'square_feet']  # change to square_feet with new database. Old dtabase had Square_feet
                        row['transaction_id'] = apt['transaction_id']
                        row['start_date'] = l['start_date']
                        row['end_date'] = l['end_date']
                        print(row)
                        table.append(row)
                        row = {}
    return table

# Add this view
class DataView(TemplateView):

    def get(self, request, **kwargs):
        try:
            if request.session['username']!=None:
                cursor = connection.cursor()
                # company
                cursor.execute('SELECT * from company')
                comp = dictfetchall(cursor)
                print('comp')

                # lease_tenants
                cursor.execute('SELECT * from lease_tenants')
                tenants = dictfetchall(cursor)
                print('ten')

                # manager_phone
                cursor.execute('SELECT * from manager_phone')
                m_phone = dictfetchall(cursor)
                print('mp')

                # property
                cursor.execute('SELECT * from property')
                properties = dictfetchall(cursor)
                print('prop')

                # mangers
                cursor.execute('SELECT * from manager')
                managers = dictfetchall(cursor)
                print('man')
                print(managers)

                # manages
                cursor.execute('SELECT * from manages')
                manage_props = dictfetchall(cursor)
                print('mans')
                print(manage_props)

                # amenities
                cursor.execute('SELECT * from amenities')
                amenities_list = dictfetchall(cursor)
                print('am')

                # provides_amenities
                cursor.execute('SELECT * from provides')
                provides_amenities = dictfetchall(cursor)
                print('provs')

                # apartment
                cursor.execute('SELECT * from apartment')
                apartments = dictfetchall(cursor)
                print('apt')

                # lease
                cursor.execute('SELECT * from lease')
                leases = dictfetchall(cursor)
                print('le')

                # apartment_parking_spots
                cursor.execute('SELECT * from apartment_parking_spots')
                spots = dictfetchall(cursor)
                print('sp')

                # vehicle
                cursor.execute('SELECT * from vehicle')
                vehicles = dictfetchall(cursor)
                print('v')
                cursor.close()

                general_table = create_general_table(properties, apartments, manage_props, managers, provides_amenities,
                                                     amenities_list, leases)

                return render(request, 'data.html', {'comp': comp, 'tenants': tenants, 'm_phone': m_phone, 'properties':
                    properties, 'managers': managers, 'manage_props': manage_props, 'amenities': amenities_list, 'provides':
                    provides_amenities, 'apartments': apartments, 'leases': leases, 'parking_spots': spots, 'vehicles': vehicles, 'general_table': general_table})
            else:
                print("ugh")
                return redirect('loginPage')
        except:
            print("nope")
            return redirect('loginPage')

    def update_managers_table(request):
        if request.method == "POST":
            e_id = request.POST.get("employee-id")
            f_name = request.POST.get("fname")
            l_name = request.POST.get("lname")
            email = request.POST.get("email")

            cursor = connection.cursor()
            cursor.execute("UPDATE manager SET employee_id=%s, first_name=%s, last_name=%s, email=%s WHERE employee_id=%s", [e_id,f_name,l_name,email,e_id])
        return redirect("/../data")

    def delete_managers_table(request):
        if request.method == "POST":
            e_id = request.POST.get("employee_id")

            cursor = connection.cursor()
            cursor.execute("DELETE FROM manager WHERE employee_id=%s", [e_id])
        return redirect("/../data")

    def update_property_table(request):
        if request.method == "POST":
            pid = request.POST.get("property-id")
            p_name = request.POST.get("property-name")
            street_number = request.POST.get("street-number")
            street_name = request.POST.get("street-name")
            city = request.POST.get("city")
            state = request.POST.get("state")
            zip_code = request.POST.get("zip-code")

            cursor = connection.cursor()
            cursor.execute("UPDATE property SET property_id=%s,name=%s,street_number=%s,street_name=%s,city=%s,state=%s,zip_code=%s WHERE property_id=%s", [pid,p_name,street_number,street_name,city,state,zip_code,pid])
        return redirect("/../data")

    def delete_property_table(request):
        if request.method == "POST":
            pid = request.POST.get("property-id")

            cursor = connection.cursor()
            cursor.execute("DELETE FROM property WHERE property_id=%s", [pid])
        return redirect("/../data")

    def update_amenities_table(request):
        if request.method == "POST":
            amenities_id = request.POST.get("amenities-id")
            pet = request.POST.get("pet-friendly")
            dryer = request.POST.get("dryer-washer")
            ac = request.POST.get("ac")
            heating = request.POST.get("heating")
            internet = request.POST.get("internet")

            cursor = connection.cursor()
            cursor.execute("UPDATE amenities SET amenities_id=%s,pet_friendly=%s,dryer_washer=%s,ac=%s,heating=%s,internet=%s WHERE amenities_id=%s", [amenities_id,pet,dryer,ac,heating,internet,amenities_id])
        return redirect("/../data")

    def delete_amenities_table(request):
        if request.method == "POST":
            amenities_id = request.POST.get("amenities-id")

            cursor = connection.cursor()
            cursor.execute("DELETE FROM amenities WHERE amenities_id=%s", [amenities_id])
        return redirect("/../data")

    def update_lease_table(request):
        if request.method == "POST":
            t_id = request.POST.get("transaction-id")
            price = request.POST.get("price")
            s_date = request.POST.get("s-date")
            e_date = request.POST.get("e-date")

            cursor = connection.cursor()
            cursor.execute("UPDATE lease SET transaction_id=%s,price=%s,start_date=%s,end_date=%s WHERE transaction_id=%s", [t_id,price,s_date,e_date,t_id])
        return redirect("/../data")

    def delete_lease_table(request):
        if request.method == "POST":
            t_id = request.POST.get("transaction-id")

            cursor = connection.cursor()
            cursor.execute("DELETE FROM lease WHERE transaction_id=%s", [t_id])
        return redirect("/../data")

    def update_apartment_table(request):
        if request.method == "POST":
            p_id = request.POST.get("property-id")
            a_num = request.POST.get("a-num")
            style = request.POST.get("style")
            s_f = request.POST.get("sf")
            t_id = request.POST.get("t-id")

            cursor = connection.cursor()
            cursor.execute("UPDATE apartment SET property_id=%s,apartment_number=%s,style=%s,square_feet=%s,transaction_id=%s WHERE property_id=%s AND apartment_number=%s", [p_id,a_num,style,s_f,t_id,p_id,a_num])
        return redirect("/../data")

    def delete_apartment_table(request):
        if request.method == "POST":
            p_id = request.POST.get("p-id")
            a_num = request.POST.get("a-num")

            cursor = connection.cursor()
            cursor.execute("DELETE FROM apartment WHERE property_id=%s AND apartment_number=%s",[p_id,a_num])
        return redirect("/../data")

    def update_provides_table(request):
        if request.method == "POST":
            p_id = request.POST.get("property-id")
            a_id = request.POST.get("a-id")

            cursor = connection.cursor()
            cursor.execute("UPDATE provides SET amenities_id=%s WHERE property_id=%s",[a_id,p_id])
        return redirect("/../data")

    def delete_provides_table(request):
        if request.method == "POST":
            p_id = request.POST.get("property-id")

            cursor = connection.cursor()
            cursor.execute("DELETE FROM provides WHERE property_id=%s", [p_id])
        return redirect("/../data")

    def update_manages_table(request):
        if request.method == "POST":
            p_id = request.POST.get("p-id")
            e_id = request.POST.get("e-id")

            cursor = connection.cursor()
            cursor.execute("UPDATE manages SET employee_id =%s WHERE property_id=%s", [e_id,p_id])
        return redirect("/../data")

    def delete_manages_table(request):
        if request.method == "POST":
            p_id = request.POST.get("p-id")

            cursor = connection.cursor()
            cursor.execute("DELETE FROM manages WHERE property_id=%s", [p_id])
        return redirect("/../data")

    def get_apt_info(request):
        if request.method == "POST":
            p_id = request.POST.get("property-id")

            cursor = connection.cursor()
            cursor.execute("CALL getProp_apartment(%s)", [p_id])
            apt_info = dictfetchall(cursor)

        return render(request, "tables/stored_procedure_info.html", {'apt_info':apt_info})
        

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