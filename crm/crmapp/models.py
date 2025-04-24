from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Agent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    address = models.TextField()
    phone = models.CharField(max_length=10, unique=True)
    location = models.CharField(max_length=100, null=True, blank=True) 
    profileimage = models.ImageField(upload_to='agent_profile/', null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    pin_code = models.CharField(max_length=6, null=True, blank=True) 


class Clients(models.Model):
    agent = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    age = models.PositiveIntegerField()
    dob = models.DateField()
    profession = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2)
    adhar_card = models.CharField(max_length=12)
    pan_card = models.CharField(max_length=10)
    has_kids = models.BooleanField()
    source_of_information = models.CharField(max_length=200)
    customer_service_satisfaction = models.TextField()
    claim_satisfaction = models.TextField()
    insurance_markup_area = models.CharField(max_length=200)
    agent_visited_policy = models.CharField(max_length=200) 
    willingness_to_purchase = models.BooleanField()
    customer_preferences = models.TextField()
    willingness_to_switch = models.BooleanField()
    existing_company_name = models.CharField(max_length=100, blank=True, null=True)
    existing_insurance_name = models.CharField(max_length=100, blank=True, null=True)
    existing_claim_status = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)




class Campaign(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    poster = models.ImageField(upload_to='poster/', null=True, blank=True)
    start_date = models.DateField()
    time = models.TimeField(default='00:00:00')
    location = models.CharField(max_length=100, null=True, blank=True)
    agent = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Clientcampaign(models.Model):
   agent = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
   client = models.ForeignKey(Clients,on_delete=models.CASCADE,null=True,blank=True)
   campaign=models.ForeignKey(Campaign,on_delete=models.CASCADE,null=True,blank=True)
