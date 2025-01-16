from django.db import models
from  django.contrib.auth.models import User

class Income(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    yearly_cost = models.IntegerField(null=True)
    monthly_cost = models.IntegerField(null=True)
    weekly_cost = models.IntegerField(null=True)
    offset = models.IntegerField(null=True)
    yearly_increase = models.IntegerField(null=True)

