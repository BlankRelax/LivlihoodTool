from rest_framework.generics import CreateAPIView

from apps.livelihood.serializers.income_create import CreateIncomeSerializer
from apps.livelihood.models.income import Income
class CreateIncomeView(CreateAPIView):
    serializer_class = CreateIncomeSerializer
    queryset= Income.objects.all()
