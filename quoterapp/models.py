from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    rut = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    mail = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name or f"Client {self.id}"

class Brand(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name or f"Brand {self.id}"
    
class VehicleType(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)  # Liviano/Pesado

    def __str__(self):
        return self.name or f"VehicleType {self.id}"

class Model(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name or f"Model {self.id}"

class Vehicle(models.Model):
    license_plate = models.CharField(max_length=255, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    usage_type = models.CharField(max_length=255, null=True, blank=True)  # Puede ser un campo con opciones

    def __str__(self):
        return self.license_plate or f"Vehicle {self.id}"

class Company(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name or f"Company {self.id}"

class CompanyPlan(models.Model):
    code = models.CharField(max_length=255, null=True, blank=True)
    deductible = models.IntegerField(null=True, blank=True)
    premium = models.IntegerField(null=True, blank=True)
    installment_count = models.IntegerField(null=True, blank=True)
    validity = models.DateField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.code or f"CompanyPlan {self.id}"

class Quote(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    company_plan = models.ForeignKey(CompanyPlan, on_delete=models.CASCADE)
    validity = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Quote {self.id} - {self.client.name if self.client.name else self.client.id}"