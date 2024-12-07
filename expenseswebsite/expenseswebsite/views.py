from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from datetime import datetime, date
from django.http import JsonResponse


# Import the necessary models
from expenses.models import Expense
from userincome.models import UserIncome

@login_required(login_url='/authentication/login')
def dashboard(request):
    transactions = []
    incomes = UserIncome.objects.filter(owner=request.user).values('date', 'amount', 'description')[:30]
    expenses = Expense.objects.filter(owner=request.user).values('date', 'amount', 'description')[:30]
    for income in incomes:
        transactions.append({
            'date': income['date'],
            'type': 'Income',
            'amount': income['amount'],
            'description': income['description']
        })
    for expense in expenses:
        transactions.append({
            'date': expense['date'],
            'type': 'Expense',
            'amount': expense['amount'],
            'description': expense['description']
        })
    transactions.sort(key=lambda x: x['date'], reverse=True)
    return render(request, 'dashboard.html', {'transactions': transactions})









@login_required(login_url='/authentication/login')
def dashboard_data(request):
    today = date.today()
    start_of_year = today.replace(month=1, day=1)

    incomes = UserIncome.objects.filter(owner=request.user, date__gte=start_of_year).values('date', 'amount')
    expenses = Expense.objects.filter(owner=request.user, date__gte=start_of_year).values('date', 'amount')

    monthly_summary_data = defaultdict(lambda: {'income': 0, 'expense': 0})

    for income in incomes:
        month_key = f"{income['date'].year}-{income['date'].month:02d}"
        monthly_summary_data[month_key]['income'] += income['amount']

    for expense in expenses:
        month_key = f"{expense['date'].year}-{expense['date'].month:02d}"
        monthly_summary_data[month_key]['expense'] += expense['amount']

    monthly_data = [
        {'month': month, 'income': data['income'], 'expense': data['expense']}
        for month, data in sorted(monthly_summary_data.items())
    ]

    return JsonResponse({'monthly_data': monthly_data})
