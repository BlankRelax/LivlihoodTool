"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include

from apps.livelihood.views.income_create import CreateIncomeView
from apps.livelihood.views.expense_create import CreateExpenseView
from apps.livelihood.views.expense_delete import DeleteExpenseView
from apps.livelihood.views.income_delete import DeleteIncomeView
from apps.livelihood.views.plot_net import PlotNetView
from apps.livelihood.views.ai_summary import AISummary
from apps.livelihood.views.home import home, assets_and_liabilities, ai_summary

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home),
    path('assets_and_liabilities/', assets_and_liabilities),
    path('ai_summary/', ai_summary),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/livelihood/users/<int:user_id>/income/', CreateIncomeView.as_view(), name='create_income_view'),
    path('api/livelihood/users/<int:user_id>/expense/', CreateExpenseView.as_view(), name='create_expense_view'),
    path('api/livelihood/users/<int:user_id>/expense/income/', PlotNetView.as_view(), name='plot_net_view'),
    path('api/livelihood/income/', DeleteIncomeView.as_view(), name='delete_income_view'),
    path('api/livelihood/expense/', DeleteExpenseView.as_view(), name='delete_expense_view'),
    path('api/livelihood/users/<int:user_id>/expense/income/summarize/', AISummary.as_view(), name='ai_summary_view'),

]
