import urllib.parse
from rest_framework import views
from django.shortcuts import get_list_or_404, render
from rest_framework.permissions import AllowAny
import io
import urllib, base64


from apps.livelihood.models import Income, Expense
from apps.livelihood.backend import base
class PlotNetView(views.APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def init_objects(self,user_expenses:list[Expense],user_incomes:list[Income]):
        expense_objects=[base.Expense(yearly_cost=user_expense.yearly_cost, monthly_cost=user_expense.monthly_cost, weekly_cost=user_expense.weekly_cost) for user_expense in user_expenses]
        income_objects=[base.Income(yearly=user_income.yearly_cost, monthly=user_income.monthly_cost, weekly=user_income.weekly_cost, offset=user_income.offset, yearly_increase=user_income.yearly_increase) for user_income in user_incomes]
        return expense_objects, income_objects
    
    def get(self, request, user_id):
        user_expenses = get_list_or_404(Expense.objects.all(), user_id=user_id)
        user_incomes = get_list_or_404(Income.objects.all(), user_id=user_id)

        expense_objects,income_objects=self.init_objects(user_expenses=user_expenses, user_incomes=user_incomes)
        # TODO: implement agg of all incomes
        fig=income_objects[0].net(expense=expense_objects,plot=True,smooth_interval= 0, income=income_objects[1:])
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string= base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        return render(request, 'dashboard.html', {'data':uri})
