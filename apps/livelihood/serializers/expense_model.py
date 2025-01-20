from rest_framework import serializers
from apps.livelihood.models import Expense

class ListExpenseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'yearly_cost', 'monthly_cost', 'weekly_cost']
        
