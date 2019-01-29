import datetime
import random

from django.http import HttpResponse
from django.shortcuts import render

from centers.forms import AddCenter
from centers.models import Center, CenterHours, ManagerCenters, Discounts

from reviews.models import StarRating


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
            if (x.id == y.center_id and x.ticket_cost != 0):
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
            return render(request, "add_discount.html", {"error1": "قیمت جدید از قیمت قبلی بیشتر است!"})
        elif discounts.count() > 0 :
            for k in discounts:
                if k.expiration_date >= datetime.date.today():
                    return render(request, "add_discount.html", {"error2": "این مرکز تخفیف دارد!"})

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


def find_centers(request):
    return render(request, 'find_centers.html')
def findCenterByCategory(request):
    try:
        listCenters=[]
        all_centers = Center.objects.all()
        for center in all_centers:
            if center.type == request.POST['category']:
                listCenters.append(center)
    except (KeyError, Center.DoesNotExist):
        return render(request, 'find_centers.html',{"listCenters": listCenters,
                                                       "error_message": "error"})
    else:
        return render(request,'find_centers.html',{"listCenters": listCenters})

def findCenterByTime(request):
    from datetime import datetime
    if request.method == 'POST':
        day = request.POST.get('day')
        time = request.POST.get('time')
        centersByDay=CenterHours.objects.filter(day=day)
        timeSt = datetime.strptime(time, '%H:%M')
        returnedCenters=[]
        for a in centersByDay:
            if time >= a.open_time and time <= a.close_time and a.id not in returnedCenters:
                returnedCenters.append(a.center_id_id)
        centers=[]
        allCenters=Center.objects.all()
        centerNum = Center.objects.all().count()
        r = list(range(centerNum))
        random.shuffle(r)

        for a in r:
            for b in returnedCenters:
                if allCenters[a].id == b and len(centers) < 5:
                    centers.append(allCenters[a])


        data={
            "centers":centers,
        }

    return render(request, 'find_centers.html',data)



def centersFilters(request):

    allCenters=Center.objects.all()
    filteredCenters = allCenters
    choosedType = 'كل مراكز'
    filter = None

    centersByCost=allCenters.order_by('ticket_cost')

    rating = StarRating.objects.values_list('center_id_id', flat=True).distinct()
    centerByRate = rating.order_by('-avg_all')

    centerByDiscount1 = Discounts.objects.all()
    centerByDiscount = []
    for a in centerByDiscount1:
        if a.expiration_date >= datetime.date.today():
            centerByDiscount.append(a)
    centerByDiscount3=sorted(centerByDiscount, key=lambda Discounts: Discounts.rate)
    centerTypes = []
    centerTypes.append('None')
    centerTypes.append('كل مراكز')
    for a in allCenters:
        if a.type not in centerTypes:
            centerTypes.append(a.type)

    if request.method == 'POST':
        choosedType=request.POST.get('centerType')
        if choosedType != 'None':
            filteredCenters = Center.objects.filter(type=choosedType)
        if choosedType == 'كل مراكز':
            filteredCenters = allCenters
        filter=request.POST.get('filter')

        if filter == 'قيمت بليط':
            filteredCenters = centersByCost
            nameOfFilter = filter

        elif filter == 'امتیاز كاربران':
            centers=[]
            for a in centerByRate:
                for b in allCenters:
                    if a == b.id:
                        centers.append(b)
            for d in allCenters:
                if d not in centers:
                    centers.append(d)
            nameOfFilter = filter
            filteredCenters = centers


        elif filter == "میزان تخفیف":
           nameOfFilter = filter
           centers2=[]
           for d in centerByDiscount3:
                for e in allCenters:
                    if d.center_id_id == e.id:
                        centers2.append(e)
           filteredCenters = centers2





    if choosedType != None and filter == None:
        nameOfFilter = choosedType




    data={
        'centerTypes':centerTypes,
        'filteredCenters':filteredCenters,
        'nameOfFilter':nameOfFilter,
    }


    return render(request,'centerFilters.html',data)