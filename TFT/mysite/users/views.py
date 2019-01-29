
from random import randint
import random
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

from django.urls import reverse_lazy
from django.views import generic

import datetime
from .models import Interest, UserInterests, CenterHours, Center, ManagerCenters, Discounts
from .forms import CustomUserCreationForm, AddCenter


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

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



def interests(request):
    data2=Interest.objects.all()
    data = UserInterests.objects.all()
    fav = {
        "fav": data,
        "pos": data2
    }
    return render(request,'favorites.html',fav)

def choose_interests(request):
    current_user = request.user
    data = Interest.objects.all()
    data2 = UserInterests.objects.filter(user_id=current_user)

    z = []
    for x in data:
        flag=0
        for y in data2:
            if x.id == y.interest_id:
                flag=1

        if flag == 0 :
            z.append(x.id)
    pos = {
        "id": z,
        "pos":data
    }
    return render(request,'choose_interests.html',pos)

def get_interest_data(request):
   current_user = request.user.id
   int_id=request.POST.get("title")
   d,form = UserInterests.objects.get_or_create(interest_id=int_id,user_id=current_user)
   d.save()

   current_user = request.user
   data = Interest.objects.all()
   data2 = UserInterests.objects.filter(user_id=current_user)

   z = []
   for x in data:
       flag = 0
       for y in data2:
           if x.id == y.interest_id:
               flag = 1

       if flag == 0:
           z.append(x.id)
   pos = {
       "id": z,
       "pos": data
   }
   return render(request, 'choose_interests.html', pos)


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

def suggest_centers(request):
    counter=0
    userId=request.user.id
    userInterestNames= []
    returnedCenters= []
    userInterests=UserInterests.objects.filter(user_id=userId)
    interest=Interest.objects.all()
    centers=Center.objects.all()
    discontList=Discounts.objects.all()


    for a in userInterests:
        for b in interest:
            if a.interest_id == b.id:
                userInterestNames.append(b.name)

    if len(userInterestNames) == 0:
        for a in centers:
            if a != None and counter < 10:
                returnedCenters.append(a)
                counter=counter+1

    n=None
    if len(userInterestNames) <10 and len(userInterestNames) != 0:
        for a in range(len(userInterestNames)):
            for b in centers:
                 if userInterestNames[a] == b.type:
                    returnedCenters.append(b)

        for a in range(10-len(userInterestNames)):
            for b in centers:
                try:
                    if b not in returnedCenters:
                        n=b
                except Exception:
                    print("ERROR")
            if n not in returnedCenters:
             returnedCenters.append(n)


    if len(userInterestNames) >=10 :
        for a in userInterestNames:
            for b in centers:
                if a == b.type:
                    returnedCenters.append(b)

    returnedDiscontList=[]
    for a in discontList:
        if a.expiration_date >= datetime.date.today():
            returnedDiscontList.append(a)
    data={
        "centers": returnedCenters,
        "discontList":returnedDiscontList,
    }

    return render(request, 'suggesting_centers.html', data)


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
        for a in centers:
            if a.name == centerName:
                centerId=a.id
                centerOldCost=a.ticket_cost
                break

        rate=((int(centerOldCost)-int(newCost))/int(centerOldCost))*100
        if centerId != None and centerOldCost != None:
         d, form = Discounts.objects.get_or_create(new_cost=newCost,
                                                  expiration_date=expirationDate,
                                                  center_id_id=centerId,rate=rate)
         d.save()
         return render(request,'home.html')






    data = {
        "centerNames": z,
    }
    return render(request, 'add_discount.html', data)




def suggestPackage(request):
    from datetime import datetime
    if request.method == 'POST':
        timeFrom = request.POST.get('timeFrom')
        timeTo = request.POST.get('timeTo')
        day = request.POST.get('day')
        cost = request.POST.get('cost')

        centers=Center.objects.all()
        centersHours=CenterHours.objects.all()
        (h1, m1) = timeFrom.split(':')
        (h2, m2) = timeTo.split(':')
        numberOfHours=int(h2)- int(h1)
        m3=int(m2) - int(m1)
        if int(m3) > 30:
            numberOfHours=numberOfHours+1



        centerNum=Center.objects.all().count()
        r = list(range(centerNum))
        random.shuffle(r)
        r2 = list(range(centerNum))
        random.shuffle(r2)


        p1=[]
        ccost =0
        remainingMoney=0
        for a in r:
                for b in centersHours:
                    if centers[a].id == b.center_id_id:
                      open_time= datetime.strptime(b.open_time, '%H:%M')
                      close_time = datetime.strptime(b.close_time, '%H:%M')
                      timeF=datetime.strptime(timeFrom, '%H:%M')
                      timeT = datetime.strptime(timeTo, '%H:%M')
                      if centers[a].ticket_cost <= int(cost) and centers[a] not in p1 and ccost <= int(cost) and centers[a].ticket_cost > 0  and  b.day == day and open_time <= timeF and close_time >= timeT :
                          ccost=ccost+centers[a].ticket_cost
                          if(ccost <= int(cost) and len(p1)<numberOfHours):
                             p1.append(centers[a])
                          else: ccost=ccost-centers[a].ticket_cost
        p2 = []
        ccost2 = 0
        remainingMoney2 = 0
        for a in r2:
                for b in centersHours:
                    if centers[a].id == b.center_id_id:
                        open_time = datetime.strptime(b.open_time, '%H:%M')
                        close_time = datetime.strptime(b.close_time, '%H:%M')
                        timeF = datetime.strptime(timeFrom, '%H:%M')
                        timeT = datetime.strptime(timeTo, '%H:%M')
                        if centers[a].ticket_cost <= int(cost) and centers[a] not in p1 and centers[a] not in p2 and ccost2 <= int(
                                cost) and centers[a].ticket_cost > 0 and b.day == day and open_time <= timeF and close_time >= timeT:
                            ccost2 = ccost2 + centers[a].ticket_cost
                            if (ccost2 <= int(cost) and len(p2)<numberOfHours):
                                p2.append(centers[a])
                            else:
                                ccost2 = ccost2 - centers[a].ticket_cost

        error = None
        error2 = None
        remainingMoney=int(cost) - ccost
        remainingMoney2 = int(cost) - ccost2
        if len(p1) == 0 :
            error="Not Found"
        if len(p2) == 0:
            error2="Not Found"

        data={
            "p1":p1,
            "p2":p2,
            "remainingMoney":remainingMoney,
            "remainingMoney2": remainingMoney2,
            "error": error,
            "error2": error2,
        }
        return render(request, 'suggesting_Package.html', data)





    days=["Saturday","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday"]
    data2={
        "day":days
    }
    return render(request, 'suggest_Package.html',data2)

