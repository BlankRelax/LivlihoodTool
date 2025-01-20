from django.shortcuts import render

def home(request):
 return render(request, 'home.html')

def assets_and_liabilities(request):
 return render(request, 'assets_liabilities.html')