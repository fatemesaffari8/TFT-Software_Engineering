import datetime

from django.http import HttpResponse
from django.shortcuts import render

from centers.forms import AddCenter
from centers.models import Center, CenterHours, ManagerCenters, Discounts


def add_center(request):
    if request.method == 'POST':
        centerform = AddCenter(request.POST)
        if centerform.is_valid():
            centerform.save()
            centerid = Center.objects.latest('id')
            if request.POST.get('sat-from') !='' and request.POST.get('sat-to')!='':
                open=request.POST.get('sat-from')
                close=request.POST.get('sat-to')
                d, form = CenterHours.objects.get_or_create(center_id=centerid, day='Saturday', open_time=open,close_time=close)
                d.save()
            if request.POST.get('sun-from') !='' and request.POST.get('sun-to')!='':
                open=request.POST.get('sun-from')
                close=request.POST.get('sun-to')
                d, form = CenterHours.objects.get_or_create(center_id=centerid,day='Sunday', open_time=open,close_time=close)
                d.save()
            if request.POST.get('mon-from') !='' and request.POST.get('mon-to')!='':
                open=request.POST.get('mon-from')
                close=request.POST.get('mon-to')
                d, form = CenterHours.objects.get_or_create(center_id=centerid,day='Monday', open_time=open,close_time=close)
                d.save()
            if request.POST.get('tue-from') !='' and request.POST.get('tue-to')!='':
                open=request.POST.get('tue-from')
                close=request.POST.get('tue-to')
                d, form = CenterHours.objects.get_or_create(center_id=centerid,day='Tuesday', open_time=open,close_time=close)
                d.save()
            if request.POST.get('wed-from') !='' and request.POST.get('wed-to')!='':
                open=request.POST.get('wed-from')
                close=request.POST.get('wed-to')
                d, form = CenterHours.objects.get_or_create(center_id=centerid,day='Wednesday', open_time=open,close_time=close)
                d.save()
            if request.POST.get('thu-from') !='' and request.POST.get('thu-to')!='':
                open=request.POST.get('thu-from')
                close=request.POST.get('thu-to')
                d, form = CenterHours.objects.get_or_create(center_id=centerid,day='Thursday', open_time=open,close_time=close)
                d.save()
            if request.POST.get('fri-from') !='' and request.POST.get('fri-to')!='':
                open=request.POST.get('fri-from')
                close=request.POST.get('fri-to')
                d, form = CenterHours.objects.get_or_create(center_id=centerid,day='Friday', open_time=open,close_time=close)
                d.save()
            cuser=request.user.id
            cid=Center.objects.latest('id').id
            k,managercenter=  ManagerCenters.objects.get_or_create(center_id=int(cid),manager_id=cuser)
            k.save()


        return render(request, 'home.html')
    else:
        form = AddCenter()

    return render(request, 'add_center.html', {'form': form})



def show_centers(request):
    current_user = request.user.id
    data = Center.objects.all()
    data2 = ManagerCenters.objects.filter(manager_id=current_user)
    z = []
    for x in data:
        for y in data2:
            if(x.id==y.center_id):
                z.append(x.id)
    data3={
        "id":z,
        "center":data
    }
    return render(request, 'centers.html', data3)




def AddDiscount(request):
    current_user = request.user.id
    data1 = Center.objects.all()
    data2 = ManagerCenters.objects.filter(manager_id=current_user)
    z = []
    m= []
    for x in data1:
        for y in data2:
            if (x.id == y.center_id):
                z.append(x.name)
                m.append(x.ticket_cost)

    if request.method == 'POST':
        centerName = request.POST.get('center')
        newCost = request.POST.get('cost')
        expirationDate = request.POST.get('expiration_date')
        centers= Center.objects.all()
        if newCost == '' or expirationDate == '':
            data2 = {
                "centerNames": z,
            }
            return render(request, 'add_discount.html', data2)
        for a in centers:
            if a.name == centerName:
                centerId=a.id
                centerOldCost=a.ticket_cost
                break

        rate=((int(centerOldCost)-int(newCost))/int(centerOldCost))*100
        discounts = Discounts.objects.filter(center_id=centerId)
        if int(newCost) > centerOldCost:
            return HttpResponse('<h1>new cost > old cost , It is not discount!!!</h1>')
        elif discounts.count() > 0 :
            for k in discounts:
                if k.expiration_date >= datetime.date.today():
                    return HttpResponse('<h1>Error! This center have a discount</h1>')

        else:
            if centerId != None and centerOldCost != None:
                d, form = Discounts.objects.get_or_create(new_cost=newCost,
                                                          expiration_date=expirationDate,
                                                          center_id_id=centerId, rate=rate)
                d.save()
                return render(request, 'home.html')



    data = {
        "centerNames": z,
    }
    return render(request, 'add_discount.html', data)

