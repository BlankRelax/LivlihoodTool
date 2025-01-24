from django.db import models
from  django.contrib.auth.models import User

class Income(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    yearly_cost = models.IntegerField(null=True, default=0)
    monthly_cost = models.IntegerField(null=True, default=0)
    weekly_cost = models.IntegerField(null=True, default=0)
    offset = models.IntegerField(null=True, default=0)
    yearly_increase = models.IntegerField(null=True, default=0)
    name = models.TextField(null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

