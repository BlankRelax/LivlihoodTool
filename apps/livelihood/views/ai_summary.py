from rest_framework.views import APIView
from django.shortcuts import get_list_or_404
from django.forms.models import model_to_dict
from django.http import StreamingHttpResponse
from rest_framework.permissions import AllowAny

from apps.livelihood.backend.AI.hugging_face_chatbot import HuggingFaceChatBot

from apps.livelihood.models import Expense, Income
class AISummary(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_user_info(self,user_id)->tuple[list[dict], list[dict]]:
        user_expense = get_list_or_404(Expense.objects.all(), user_id=user_id)
        user_income = get_list_or_404(Income.objects.all(), user_id=user_id)
        expense_list = []
        income_list = []

        for expense, income in zip(user_expense, user_income):
            expense_list.append(model_to_dict(expense, fields=[field.name for field in expense._meta.fields]))
            income_list.append(model_to_dict(income, fields=[field.name for field in income._meta.fields]))
        return expense_list, income_list


    def get(self, request, user_id):
        expense_list, income_list=self.get_user_info(user_id)
        prompt = """
            Summarize this persons incomes and expenses and provide finacial advice for him
            """
        chatbot = HuggingFaceChatBot(model_name='deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B', token_env_name=None, prompt=prompt)
        streamed_output=chatbot.chat(message=f"{expense_list} {income_list}")
        return StreamingHttpResponse(streamed_output)



