from django.db.models import Sum, F
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum

from django.http import HttpRequest, HttpResponseForbidden, HttpResponse
from main.decorators import role_required
from datetime import timedelta, datetime
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status, generics # type: ignore
from django.db import transaction, IntegrityError
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from cook.models import Dish, Menu, Review, Stock, Ingredient, Composition
from main.decorators import role_required
from .models import Student, Purchases, Allergy
from .forms import StudentOrderForm, AddAllergyForm, FeedBackForm,BuyAbonimentForm, TopUpForm
from decimal import Decimal

def dish_or_0(dish: Dish):
    return dish.cost if dish else Decimal('0')

def index(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 2: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь учеником.")

    
    context = {"title": "Главная страница"}
    return render(request, "student/index.html", context)


def allergy(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 2: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь учеником.")

    
    student = request.user.student_profile
    if request.method == "POST":

        form = AddAllergyForm(request.POST)

        if form.is_valid():
            allergy = form.save(commit=False)
            allergy.student = student
            try:
                allergy.save()
                messages.success(request, "Аллергия добавлена")
                return redirect('allergy_page')
            
            except IntegrityError:
                form.add_error("ingredient", "Эта аллергия уже существует")
    
    else:
        form = AddAllergyForm()

    return render(request, "student/allergy.html", {
        "form":form,
        "allergies": Allergy.objects.filter(student=student)
        })

def allergy_delete(request: HttpRequest, allergy_id)-> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 2: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь учеником.")

    
    try:
        student = request.user.student_profile
        allergy = get_object_or_404(Allergy, id=allergy_id, student=student)
        allergy.delete()
    except:
        pass
    return redirect("allergy_page")


def FeedBack(request: HttpRequest,dish_id: int) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 2: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь учеником.")


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


def top_up(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 2: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь учеником.")
    
    student = request.user.student_profile

    if request.method == "POST":
        form = TopUpForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                summa = form.cleaned_data['summa']
                if not isinstance(summa, Decimal):
                    summa = Decimal(str(summa))
                    
                student.money += summa
                student.save()

                messages.success(request, f"Пополнение прошло успешно")
                return redirect('main_page') 
    else:
        form = TopUpForm()

    return render(request, "student/top_up.html", {"form": form})



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
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 2: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь учеником.")

    
    student = request.user.student_profile
    
    if request.GET.get('get_price') == '1':
        date = request.GET.get('date_of_meal')
        intake = request.GET.get('food_intake')
        if date and intake:
            menu = Menu.objects.filter(date=date, food_intake=intake).first()
            if menu:
                has_active_ticket = student.date and student.date >= datetime.strptime(date, '%Y-%m-%d').date()
                print(has_active_ticket)
                if has_active_ticket:
                    price = Decimal(0)
                else:
                    price = menu.get_total_cost()

                return JsonResponse({'price': float(price)})
            else:
                return JsonResponse({'price': None})
            
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    if request.method == 'POST':
        form = StudentOrderForm(request.POST)
        if form.is_valid():
            chosen_date = form.cleaned_data.get('date_of_meal')
            food_intake = form.cleaned_data.get('food_intake')
            
            menu_for_day = Menu.objects.filter(date=chosen_date, food_intake=food_intake).first()
            
            if menu_for_day is None:
                messages.error(request, f"Меню на {chosen_date} ({food_intake}) еще не сформировано.")
                return render(request, 'student/pay_onetime.html', {'form': form, 'balance': student.money})


            if Purchases.objects.filter(student=student, date_of_meal=chosen_date, food_intake=food_intake).exists():
                messages.error(request, f"Ошибка: Вы уже оплатили {food_intake} на {chosen_date}!")
                return render(request, 'student/pay_onetime.html', {'form': form, 'balance': student.money})


            has_active_ticket = student.date and student.date >= chosen_date
            
            if has_active_ticket:
                price = 0
                payment_type = "Абонемент"
            else:
                price = menu_for_day.get_total_cost()
                payment_type = "Разовая оплата"

            if not has_active_ticket and student.money < price:
                messages.error(request, f"Недостаточно средств. Стоимость: {price} руб. Ваш баланс: {student.money} руб.")
                return render(request, 'student/pay_onetime.html', {'form': form, 'balance': student.money})
            
            try:
                with transaction.atomic():

                    if not has_active_ticket:
                        student.money -= price
                        student.save()

                    order = form.save(commit=False)
                    order.student = student
                    order.menu = menu_for_day
                    order.deposited_money = price
                    order.type_of_purchase = payment_type
                    order.save()

                    messages.success(request, f"Заказ успешно оформлен через {payment_type}.")
                    return redirect('main_page')
            except Exception as e:
                messages.error(request, f"Техническая ошибка: {e}")
    else:
        form = StudentOrderForm()

    return render(request, 'student/pay_onetime.html', {
        'form': form,
        'balance': student.money
    })




def buy_season_ticket(request):
    student = request.user.student_profile
    money = student.money
    if request.method == 'POST':
        form = BuyAbonimentForm(request.POST)
        if form.is_valid():
            plan = int(form.cleaned_data.get('choise'))
            
            if not plan:
                messages.error(request, "Выбран некорректный тариф.")
                return redirect('season_ticket')
            elif plan == 7:
                price = Decimal(5000)
                days_to_add = int(7)
            elif plan == 14:
                price = Decimal(10000)
                days_to_add = int(14)
            elif plan == 30:
                price = Decimal(20000)
                days_to_add = int(30)
            elif plan == 90:
                price = Decimal(60000)
                days_to_add = int(90)
            elif plan == 180:
                price = Decimal(120000)
                days_to_add = int(180)
            elif plan == 270:
                price = Decimal(150000)
                days_to_add = int(270)

            money = student.money

            if money < price:
                messages.error(request, f"Недостаточно средств. Стоимость тарифа: {price} руб.")
            else:
                student.money -= price

                abdate= student.date
                today = timezone.now().date()
                if abdate is not None:
                    if abdate > today :
                        student.date = abdate + timedelta(days=days_to_add)
                    else:
                        student.date = today + timedelta(days=days_to_add)
                else:
                    student.date = today + timedelta(days=days_to_add)

                student.save()
                    
                messages.success(request, f"Оплачено! Абонемент активен")
                return redirect('main_page')
        else:
            messages.error(request, "Ошибка валидации формы. Попробуйте еще раз.")
    else:
        form = BuyAbonimentForm()

    return render(request, 'student/season_ticket.html', {'form': form, 'student': student, 'aboba' : money})

def Menu_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 2: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь учеником.")

    student = request.user.student_profile
    now = timezone.now().date()

    allergies_object = Allergy.objects.filter(student=student)
    allergies_ingredients = [allergy.ingredient for allergy in allergies_object]

    m1_breakfast = Menu.objects.filter(date=now - timedelta(days=1), food_intake="Завтрак").first()
    m1_lunch = Menu.objects.filter(date=now - timedelta(days=1),food_intake="Обед").first()

    m2_breakfast = Menu.objects.filter(date=now, food_intake="Завтрак").first()
    m2_lunch = Menu.objects.filter(date=now,food_intake="Обед").first()

    m3_breakfast = Menu.objects.filter(date=now + timedelta(days=1), food_intake="Завтрак").first()
    m3_lunch = Menu.objects.filter(date=now + timedelta(days=1),food_intake="Обед").first()

    m4_breakfast = Menu.objects.filter(date=now + timedelta(days=2), food_intake="Завтрак").first()
    m4_lunch = Menu.objects.filter(date=now + timedelta(days=2),food_intake="Обед").first()
    
    m5_breakfast = Menu.objects.filter(date=now + timedelta(days=3), food_intake="Завтрак").first()
    m5_lunch = Menu.objects.filter(date=now + timedelta(days=3),food_intake="Обед").first()

    m6_breakfast = Menu.objects.filter(date=now + timedelta(days=4), food_intake="Завтрак").first()
    m6_lunch = Menu.objects.filter(date=now + timedelta(days=4),food_intake="Обед").first()

    m7_breakfast = Menu.objects.filter(date=now + timedelta(days=5), food_intake="Завтрак").first()
    m7_lunch = Menu.objects.filter(date=now + timedelta(days=5),food_intake="Обед").first()

    price1_breakfast = m1_breakfast.get_total_cost() if m1_breakfast else 0
    price1_lunch = m1_lunch.get_total_cost() if m1_lunch else 0

    price2_breakfast = m2_breakfast.get_total_cost() if m2_breakfast else 0
    price2_lunch = m2_lunch.get_total_cost() if m2_lunch else 0

    price3_breakfast = m3_breakfast.get_total_cost() if m3_breakfast else 0
    price3_lunch = m3_lunch.get_total_cost() if m3_lunch else 0

    price4_breakfast = m4_breakfast.get_total_cost() if m4_breakfast else 0
    price4_lunch = m4_lunch.get_total_cost() if m4_lunch else 0

    price5_breakfast = m5_breakfast.get_total_cost() if m5_breakfast else 0
    price5_lunch = m5_lunch.get_total_cost() if m5_lunch else 0

    price6_breakfast = m6_breakfast.get_total_cost() if m6_breakfast else 0
    price6_lunch = m6_lunch.get_total_cost() if m6_lunch else 0

    price7_breakfast = m7_breakfast.get_total_cost() if m7_breakfast else 0
    price7_lunch = m7_lunch.get_total_cost() if m7_lunch else 0

    days_data = [
        {
            'title': 'Вчера',
            'meals': [
                    {'name': 'Завтрак', 'menu':m1_breakfast, 'price': price1_breakfast},
                    {'name': 'Обед', 'menu': m1_lunch, 'price': price1_lunch},
                ],
        },

        {
            'title': 'Сегодня',
            'meals': [
                {'name': 'Завтрак', 'menu':m2_breakfast, 'price': price2_breakfast},
                {'name': 'Обед', 'menu': m2_lunch, 'price': price2_lunch},
            ],
        },

        {
            'title': 'Завтра',
            'meals': [
                {'name': 'Завтрак', 'menu':m3_breakfast, 'price': price3_breakfast},
                {'name': 'Обед', 'menu': m3_lunch, 'price': price3_lunch},
            ],
        },

        {
            'title': 'Послезавтра',
            'meals': [
                {'name': 'Завтрак', 'menu':m4_breakfast, 'price': price4_breakfast},
                {'name': 'Обед', 'menu': m4_lunch, 'price': price4_lunch},
            ],
        },

        {
            'title': 'Через 3 дня',
            'meals': [
                {'name': 'Завтрак', 'menu':m5_breakfast, 'price': price5_breakfast},
                {'name': 'Обед', 'menu': m5_lunch, 'price': price5_lunch},
            ],
        },

        {
            'title': 'Через 4 дня',
            'meals': [
                {'name': 'Завтрак', 'menu':m6_breakfast, 'price': price6_breakfast},
                {'name': 'Обед', 'menu': m6_lunch, 'price': price6_lunch},
            ],
        },

        {
            'title': 'Через 5 дней',
            'meals': [
                {'name': 'Завтрак', 'menu':m7_breakfast, 'price': price7_breakfast},
                {'name': 'Обед', 'menu': m7_lunch, 'price': price7_lunch},
            ],
        }
    ]
                

    return render(request, 'student/menu.html', {
        'balance': student.money,
        'days': days_data,
        "allergies": allergies_ingredients,
    })
























