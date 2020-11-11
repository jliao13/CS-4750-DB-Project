from django.db import models

class lease_tenants(models.Model):
    transaction_id = models.IntegerField(primary_key=True, null=False)
    tenant_name = models.CharField(max_length=255, null=False)
    class Meta:
        db_table = 'lease_tenants'
        unique_together = (('transaction_id','tenant_name'),)

class manager_phone(models.Model):
    employee_id = models.IntegerField(primary_key=True, null=False)
    phone_number = models.CharField(max_length=255, null=False)
    class Meta:
        db_table = 'manager_phone'
        unique_together = (('employee_id','phone_number'),)

class manages(models.Model):
    property_id = models.IntegerField(primary_key=True, null=False)
    employee_id = models.IntegerField(null=False)
    class Meta:
        db_table = 'manages'

class property(models.Model):
    property_id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=255, null=False)
    street_number = models.IntegerField(null=False)
    street_name = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=255, null=False)
    state = models.CharField(max_length=255, null=False)
    zip_code = models.IntegerField(null=False)    
    class Meta:
        db_table = 'property'

class company(models.Model):
    user_id = models.IntegerField(primary_key=True, null=False)
    user_name = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)
    class Meta:
        db_table = 'company'
        db_table = 'company'

class apartment_parking_spots(models.Model):
    property_id = models.IntegerField(primary_key=True, null=False)
    parking_spot = models.IntegerField(null=False)
    apartment_number = models.IntegerField(null=False)
    class Meta: 
        db_table = 'apartment_parking_spots'
        unique_together = (('property_id','parking_spot'),)

class provides(models.Model):
    property_id = models.IntegerField(primary_key=True, null=False)
    amenities_id = models.IntegerField(null=False)
    class Meta: 
        db_table = 'provides'
        unique_together = (('property_id','amenities_id'),)

class amenities(models.Model):
    amenities_id = models.IntegerField(primary_key=True, null=False)
    pet_friendly = models.BooleanField(null=False)
    dryer_washer = models.BooleanField(null=False)
    ac = models.BooleanField(null=False)
    heating = models.BooleanField(null=False)
    internet = models.BooleanField(null=False)
    class Meta:
        db_table = 'amenities'

class vehicle(models.Model):
    license_plate = models.CharField(max_length=255, primary_key=True, null=False)
    model = models.CharField(max_length=255, null=True)
    brand = models.CharField(max_length=255, null=True)
    transaction = models.ForeignKey(lease_tenants, on_delete=models.CASCADE)
    class Meta:
        db_table = 'vehicle'

class lease(models.Model):
    transaction_id = models.IntegerField(primary_key=True, null=False)
    price = models.FloatField(null=False)
    start_date = models.CharField(max_length=255, null=True)
    end_date = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(company, on_delete=models.CASCADE)
    class Meta:
        db_table = 'lease'

class manager(models.Model):
    employee_id = models.IntegerField(primary_key=True, null=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(company, on_delete=models.CASCADE)
    class Meta:
        db_table = 'manager'

    def __eq__(self, other):
        values = [(k, v) for k, v in self.__dict__.items() if k != '_state']
        other_values = [(k, v) for k, v in other.__dict__.items() if k != '_state']
        return values == other_values

class apartment(models.Model):
    property_id = models.IntegerField(primary_key=True, null=False)
    apartment_number = models.IntegerField(null=False)
    style = models.CharField(max_length=255, null=False)
    square_feet = models.IntegerField(null=False)
    transaction = models.ForeignKey(lease_tenants, on_delete=models.CASCADE)
    class Meta:
        db_table = 'apartment'
        unique_together = (('property_id','apartment_number'),)


