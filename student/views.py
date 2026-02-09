from django.db.models import Sum, F
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction, IntegrityError
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from cook.models import Dish, Menu, Review, Stock, Ingredient
from main.decorators import role_required
from .models import Student, Purchases, Allergy
from .forms import StudentOrderForm, AddAllergyForm, FeedBackForm

@role_required('Student')
def index(request: HttpRequest) -> HttpResponse:
    context = {"title": "Главная страница"}
    return render(request, "student/index.html", context)

def menu(request: HttpRequest) -> HttpResponse:
    context = {"dishes" : Dish.objects.all()}
    return render(request, "student/menu.html", context)

def allergy(request: HttpRequest) -> HttpResponse:

    student = request.user.student_profile
    if request.method == "POST":

        form = AddAllergyForm(request.POST)

        if form.is_valid():
            allergy = form.save(commit=False)
            allergy.student = student
            try:
                allergy.save()
                return redirect('allergy_page')
            except IntegrityError:
                form.add_error(None, "Эта аллергия уже существует")
    
    else:
        form = AddAllergyForm()

    return render(request, "student/allergy.html", {
        "form":form,
        "allergies": Allergy.objects.filter(student=student)
        })
def top_up(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "student/top_up.html", context)

def season_ticket(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "student/season_ticket.html", context)



def allergy_delete(request: HttpRequest, allergy_id)-> HttpResponse:
    try:
        student = request.user.student_profile
        allergy = get_object_or_404(Allergy, id=allergy_id, student=student)
        allergy.delete()
    except:
        pass
    return redirect("allergy_page")


def FeedBack(request: HttpRequest,dish_id: int) -> HttpResponse:
    context = {}

    student = request.user.student_profile
    dish = get_object_or_404(Dish, id=dish_id)
    if request.method == 'POST':
        form = FeedBackForm(request.POST)
        if form.is_valid():
            new_komment = Review()

            mark = form.cleaned_data.get('mark')
            comment = form.cleaned_data.get('comment')
            new_komment.comment = comment
            new_komment.mark = mark
            new_komment.date = timezone.now()
            new_komment.dish = dish
            new_komment.student = student
            new_komment.save()
            return redirect('menu_page') 
        else:
            messages.error(request, "Ошибка: проверьте данные формы.")
    else:
        form = FeedBackForm()
    return render(request, 'student/comment.html', {
            'form': form,
            'dish': dish
        })
@login_required
def my_purchases_list(request):
    student_profile = get_object_or_404(Student, user=request.user)
    today = timezone.now().date()

    if request.method == "POST":
        purchase_id = request.POST.get("purchase_id")
        purchase = get_object_or_404(Purchases, id=purchase_id, student=student_profile)

        if not purchase.attendance:
            purchase.attendance = True
            purchase.save()

            menu = purchase.menu
            dishes = [menu.dish1, menu.dish2, menu.dish3, menu.dish4, menu.dish5]

            for dish in dishes:
                if dish:
                    stock_item, created = Stock.objects.get_or_create(
                        dish=dish,
                        date=today,
                        defaults={
                            'amount_cooked': 0, 
                            'amount_sold': 1,
                            'expiration_date': today
                        }
                    )
                    if not created:
                        stock_item.amount_sold = F('amount_sold') + 1
                        stock_item.save()
            
        return redirect('student_orders_page')

    orders = Purchases.objects.filter(student=student_profile).order_by('-date_of_meal')

    return render(request, 'student/my_orders.html', {
        'orders': orders,
        'today': today
    })





def pay_onetime(request: HttpRequest) -> HttpResponse:
    student = request.user.student_profile
    
    if request.method == 'POST':
        form = StudentOrderForm(request.POST)
        if form.is_valid():

            chosen_date = form.cleaned_data.get('date_of_meal')
            food_intake = form.cleaned_data.get('food_intake')
            menu_for_day = Menu.objects.filter(date=chosen_date, food_intake=food_intake).first()
            
            if menu_for_day is None:
                messages.error(request, f"Меню на {chosen_date} ({food_intake}) еще не сформировано.")
                return render(request, 'student/pay_onetime.html', {'form': form, 'balance': student.money})

            duplicate_order = Purchases.objects.filter(
                student=student,
                date_of_meal=chosen_date,
                food_intake=food_intake
            ).exists()

            if duplicate_order:
                messages.error(request, f"Ошибка: Вы уже оплатили {food_intake} на {chosen_date}!")
                return render(request, 'student/pay_onetime.html', {'form': form, 'balance': student.money})


            price = menu_for_day.get_total_cost()


            if student.money < price:
                messages.error(request, f"Недостаточно средств. Стоимость: {price} руб. Ваш баланс: {student.money} руб.")
            else:
                try:
                    with transaction.atomic():

                        student.money -= price
                        student.save()

                        order = form.save(commit=False)
                        order.student = student
                        order.menu = menu_for_day
                        order.deposited_money = price
                        order.type_of_purchase = "Баланс"
                        order.save()

                        messages.success(request, f"Заказ на {food_intake} ({chosen_date}) успешно оплачен.")
                        return redirect('main_page')
                except Exception as e:
                    messages.error(request, "Произошла техническая ошибка. Средства не списаны.")
    else:
        form = StudentOrderForm()

    return render(request, 'student/pay_onetime.html', {
        'form': form,
        'balance': student.money
    })

def Menu_view(request):

    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 2: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь поваром.")
    student = request.user.student_profile
    now = timezone.now().date()
    m1 = Menu.objects.filter(date=now - timedelta(days=1)).first()
    print(m1)
    print(now)
    m2 = Menu.objects.filter(date=now).first()
    m3 = Menu.objects.filter(date=now + timedelta(days=1)).first()
    m4 = Menu.objects.filter(date=now + timedelta(days=2)).first()
    m5 = Menu.objects.filter(date=now + timedelta(days=3)).first()
    m6 = Menu.objects.filter(date=now + timedelta(days=4)).first()
    m7 = Menu.objects.filter(date=now + timedelta(days=5)).first()

    price1 = m1.get_total_cost() if m1 else 0
    price2 = m2.get_total_cost() if m2 else 0
    price3 = m3.get_total_cost() if m3 else 0
    price4 = m4.get_total_cost() if m4 else 0
    price5 = m5.get_total_cost() if m5 else 0
    price6 = m6.get_total_cost() if m6 else 0
    price7 = m7.get_total_cost() if m7 else 0

    return render(request, 'student/menu.html', {
        'balance': student.money,
        'price1': price1, 
        'price2': price2, 
        'price3': price3,
        'price4': price4, 
        'price5': price5, 
        'price6': price6, 
        'price7': price7,
        'm1': m1, 
        'm2': m2, 
        'm3': m3, 
        'm4': m4, 
        'm5': m5, 
        'm6': m6, 
        'm7': m7,
    })

def FeedBack(request: HttpRequest,dish_id: int) -> HttpResponse:
    context = {}

    student = request.user.student_profile
    dish = get_object_or_404(Dish, id=dish_id)
    if request.method == 'POST':
        form = FeedBackForm(request.POST)
        if form.is_valid():
            new_komment = Review()

            mark = form.cleaned_data.get('mark')
            comment = form.cleaned_data.get('comment')
            new_komment.comment = comment
            new_komment.mark = mark
            new_komment.date = timezone.now()
            new_komment.dish = dish
            new_komment.student = student
            new_komment.save()
            return redirect('/student/menu/') 
        else:
            messages.error(request, "Ошибка: проверьте данные формы.")
    else:
        form = FeedBackForm()
    return render(request, 'student/comment.html', {
            'form': form,
            'dish': dish
        })























