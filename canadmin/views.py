from django.shortcuts import render, redirect, get_object_or_404
from main.decorators import role_required
from django.views.decorators.http import require_POST
from .models import *
from main.decorators import login_required
# from django.db.models import Sum
from django.http import HttpRequest,HttpResponseForbidden, HttpResponse
from cook.models import *
from .forms import *
from django.db.models import Sum, Count
from .get_state import *
from student.models import Purchases
from datetime import timedelta
from django.utils import timezone

# Create your views here.
def main_page(request):
    return render(request, "canadmin/main.html")

def vieworders(request: HttpRequest) -> HttpResponse:
    orderdict = Order.objects.all()
    return render(request, 'canadmin/orders.html', context={'orders': orderdict})

@require_POST
def change_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if order.status != 1:
        ingred_id = order.ingredient_id
        ingred = get_object_or_404(Ingredient, pk=ingred_id)
        ingred.amount += order.amount
        ingred.save()
        # new_status = request.POST.get("status")
        # if new_status:
        order.status = 1
        order.save()
    return redirect('admin_view_orders')

# @login_required('Admin')
def registration(request):
    try:
        if request.user.role.title != 'Admin':
            return HttpResponseForbidden("Нет доступа")
    except:
        return HttpResponseForbidden("Нет доступа")
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # login(request, user)  # auto login after registration
            return redirect("admin_main_page")  # redirect to homepage
    else:
        form = UserRegistrationForm()
    return render(request, "canadmin/registration.html", {"form": form})


def actions(request):
    # Attributes attendance, date, date_of_meal, deposited_money, food_intake, id, menu, menu_id, student, student_id, type_of_purchase
    start_date = request.GET.get("start")
    end_date = request.GET.get("end")

    purchases = Purchases.objects.all()
    if start_date and end_date:
        purchases = purchases.filter(date__range=[start_date, end_date])
    # print(purchases.values)
    total_orders = purchases.count()
    unique_students = len(list(purchases.values_list('student_id', flat=True).distinct()))
    total_attendance = purchases.filter(attendance=True).count()
    total_money = purchases.aggregate(Sum("deposited_money"))["deposited_money__sum"] or 0

    context = {
        "total_buyers": unique_students,
        "total_orders": total_orders,
        "total_attendance": total_attendance,
        "unique_students": unique_students,
        "total_attendance": total_attendance,
        "total_money": total_money,
        "start_date": start_date,
        "end_date": end_date,
    }
    return render(request, 'canadmin/actions.html', context)


def statistic(request):
    purchases = Purchases.objects.all()
    purchases = gets_dict(purchases)
    stat = {}
    for date, get in purchases.items():
        stat[date] = get

    return render(request, "canadmin/statistic.html", {"statistic": stat})
def ingredadd(request):
    if request.method == 'POST':
        form = IngredAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ingredient_list')
    else:
        form = IngredAddForm()
    return render(request, 'canadmin/addingred.html', {'form': form})
def ingredient_list(request):
    ingredients = Ingredient.objects.all().order_by('title')
    return render(request, 'canadmin/ingredient_list.html', {'ingredients': ingredients})
def dishes_list(request):
    dishes = Dish.objects.all().order_by('title')
    return render(request, 'canadmin/dishes_list.html', {'dishes': dishes})
def dishadd(request):
    if request.method == 'POST':
        form = AddNewDishForm(request.POST, request.FILES)
        if form.is_valid():
            dish = form.save(commit=False)
            formset = CompositionFormSet(request.POST, instance=dish)
            if formset.is_valid():
                dish.save()
                for subform in formset:
                    if subform.cleaned_data.get('ingredient') and subform.cleaned_data.get('weight'):
                        comp = subform.save(commit=False)
                        comp.dish = dish
                        comp.save()
                return redirect('dishes_list')
    else:
        form = AddNewDishForm()
        formset = CompositionFormSet()
    return render(request, 'canadmin/adddish.html', {'form': form, 'formset': formset})
def Menu_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 1: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь админом.")

    now = timezone.now().date()

    titles = [
        "Вчера",
        "Сегодня",
        "Завтра",
        "Послезавтра",
        "Через 3 дня",
        "Через 4 дня",
        "Через 5 дней",
    ]

    days_data = []
    for i, title in enumerate(titles, start=-1):
        date = now + timedelta(days=i)
        breakfast = Menu.objects.filter(date=date, food_intake="Завтрак").first()
        lunch = Menu.objects.filter(date=date, food_intake="Обед").first()

        day_info = {
            "title": title,
            "meals": [
                {"name": "Завтрак", "menu": breakfast, "price": breakfast.get_total_cost() if breakfast else 0},
                {"name": "Обед", "menu": lunch, "price": lunch.get_total_cost() if lunch else 0},
            ],

        }
        days_data.append(day_info)

    return render(request, "canadmin/menu.html", {"days": days_data})
