
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference
import datetime
from collections import defaultdict


def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    
    # Fetch expenses and order them by date in descending order
    expenses = Expense.objects.filter(owner=request.user).order_by('-date')
    
    # Paginate the ordered expenses
    paginator = Paginator(expenses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch user currency preference
    currency = UserPreference.objects.get(user=request.user).currency

    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }
    
    return render(request, 'expenses/index.html', context)



@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(owner=request.user, amount=amount, date=date,
                               category=category, description=description)
        messages.success(request, 'Expense saved successfully')

        return redirect('expenses')


@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/edit-expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense. date = date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, 'Expense updated  successfully')

        return redirect('expenses')


def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')


def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'expenses/stats.html')




@login_required(login_url='/authentication/login')
def monthly_expense_summary(request):
    # Get today's date and calculate the range of 12 months (1 year) for the data
    today = datetime.date.today()
    start_of_year = today.replace(month=1, day=1)

    # Filter expenses for the current user in the last 12 months
    # Make sure to retrieve both 'date' and 'amount'
    expenses = Expense.objects.filter(
        owner=request.user, date__gte=start_of_year
    ).values('date', 'amount')

    # Prepare a dictionary to store the sum of expenses for each month
    monthly_expenses = defaultdict(float)

    for expense in expenses:
        # Get year and month from the expense's date
        month = expense['date'].month
        year = expense['date'].year

        # Create a key like "2024-01" for January 2024
        month_key = f"{year}-{month:02d}"

        # Accumulate the expenses for that month
        monthly_expenses[month_key] += expense['amount']

    # Convert the dictionary to a list of dicts that we can return in the JsonResponse
    monthly_expense_data = [{'month': month, 'total_expense': total} for month, total in monthly_expenses.items()]

    # Return the data as JSON
    return JsonResponse({'monthly_expenses': monthly_expense_data}, safe=False)