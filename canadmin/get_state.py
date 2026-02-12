from django.db.models import Sum, Count
from datetime import date 

def gets_dict(purch):
    days = []
    for obj in purch.values("date"):
        tg = [obj["date"].year, obj["date"].month, obj["date"].day]
        if not tg in days:
            days.append(tg)
    plot = dict()
    print(days)
    for target in days:
        day_date = date(*target)
        total_bud = (purch.filter(date__date=day_date).aggregate(Sum('deposited_money'))["deposited_money__sum"])
        plot[str(day_date)] = int(total_bud)
    print(plot)
    return plot
def paid_dict():
    pass