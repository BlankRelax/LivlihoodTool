from rest_framework import serializers

from apps.livelihood.models.expense import Expense

class CreateExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['yearly_cost', 'monthly_cost', 'weekly_cost', 'name', 'description']

    yearly_cost = serializers.IntegerField(required=False, allow_null=True)
    monthly_cost = serializers.IntegerField(required=False, allow_null=True)
    weekly_cost = serializers.IntegerField(required=False, allow_null=True)
    name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)