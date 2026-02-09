from django.shortcuts import render, redirect, get_object_or_404
from main.decorators import role_required
from django.views.decorators.http import require_POST
from .models import *
from main.decorators import login_required
# from django.db.models import Sum
from django.http import HttpRequest,HttpResponseForbidden, HttpResponse
from cook.models import *
from .forms import *

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
    actions = {}
    return render(request, 'canadmin/actions.html', context=actions)