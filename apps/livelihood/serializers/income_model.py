from rest_framework import serializers
from apps.livelihood.models import Income
from rest_framework.viewsets import ModelViewSet

class ListIncomeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'yearly_cost', 'monthly_cost', 'weekly_cost', 'offset', 'yearly_increase', 'name', 'description']
        
