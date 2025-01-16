from rest_framework import serializers

from apps.livelihood.models.income import Income

class CreateIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['yearly_cost', 'monthly_cost', 'weekly_cost', 'offset', 'yearly_increase']

    yearly_cost = serializers.IntegerField(required=False, allow_null=True)
    monthly_cost = serializers.IntegerField(required=False, allow_null=True)
    weekly_cost = serializers.IntegerField(required=False, allow_null=True)
    offset = serializers.IntegerField(required=False, allow_null=True)
    yearly_increase = serializers.IntegerField(required=False, allow_null=True)