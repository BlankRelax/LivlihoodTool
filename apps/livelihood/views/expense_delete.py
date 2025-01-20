from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.livelihood.models import Expense

class DeleteExpenseView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def delete(self, request):
        selected_pks = request.data.get('selected_pks')
        for pk in selected_pks:
            instance = get_object_or_404(Expense.objects.all(), id=pk)
            instance.delete()
        return Response("Deleted", status=status.HTTP_200_OK)
    
    


