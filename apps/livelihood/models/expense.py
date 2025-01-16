from django.db import models
from  django.contrib.auth.models import User

class Expense(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    yearly_cost = models.IntegerField(null=True)
    monthly_cost = models.IntegerField(null=True)
    weekly_cost = models.IntegerField(null=True)
