from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_list_or_404
from rest_framework.permissions import AllowAny

from apps.livelihood.serializers.expense_create import CreateExpenseSerializer
from apps.livelihood.serializers.expense_model import ListExpenseModelSerializer
from apps.livelihood.models import Expense
class CreateExpenseView(CreateAPIView):
    serializer_class = CreateExpenseSerializer
    queryset= Expense.objects.all()
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def create(self, request, user_id,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['user_id']=user_id
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get(self, request, user_id):
        expenses_of_user = get_list_or_404(Expense.objects.all(), user_id=user_id)
        serializer = ListExpenseModelSerializer(instance=expenses_of_user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


