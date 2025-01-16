from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from apps.livelihood.serializers.income_create import CreateIncomeSerializer
from apps.livelihood.models.income import Income
class CreateIncomeView(CreateAPIView):
    serializer_class = CreateIncomeSerializer
    queryset= Income.objects.all()

    def create(self, request, user_id,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['user_id']=user_id
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


