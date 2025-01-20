from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from apps.livelihood.serializers import income_model
from django.shortcuts import get_list_or_404
from apps.livelihood.models import Income

class IncomeModelViewSet(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def get(self, request, user_id):
        
        incomes_of_user = get_list_or_404(Income.objects.all(), user_id=user_id)
        serializer = income_model.ListIncomeModel(incomes_of_user)
        return Response(serializer.data, status=status.HTTP_200_OK)


