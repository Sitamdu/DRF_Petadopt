from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pet(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    image = models.ImageField(upload_to='media')
    sex = models.CharField(max_length=50, choices=[('male','male'), ('female','female')])
    color = models.CharField(max_length=50)
    adoption_status = models.BooleanField(default=False)
    size = models.CharField(max_length=20, choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')])

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

class Product(models.Model):
    Prod_code = models.CharField(max_length=20, unique=True)
    prod_name = models.CharField(max_length=100)
    prod_type = models.CharField(max_length=50)
    prod_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.prod_name

class AdoptionRequest(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoption_requests')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoption_requests')
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])

    def __str__(self):
        return f"Adoption Request for {self.pet.name} by {self.requester.username}"

