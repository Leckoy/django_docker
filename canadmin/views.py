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

# Create your views here.
def main_page(request):
    return render(request, "canadmin/main.html")

def vieworders(request: HttpRequest) -> HttpResponse:
    orderdict = Order.objects.all()
    return render(request, 'canadmin/orders.html', context={'orders': orderdict})

@require_POST
def change_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    new_status = request.POST.get("status")
    if new_status:
        order.status = new_status
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
    context={"gets": gets_dict(purchases)}
    # print(purchases.values("date"))
    return render(request, "canadmin/statistic.html", context)