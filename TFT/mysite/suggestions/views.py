import datetime
import random

from django.shortcuts import render

from users.models import UserInterests

from interests.models import Interest

from centers.models import Center,CenterHours,Discounts



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


    if request.method == 'POST':
        centerID = request.POST.get("details")
        data2={
            "centerId":centerID,

        }
        return render(request,'center_actions_and_details.html',data2)

    return render(request, 'suggesting_centers.html', data)





def suggestPackage(request):
    from datetime import datetime
    if request.method == 'POST':
        timeFrom = request.POST.get('timeFrom')
        timeTo = request.POST.get('timeTo')
        day = request.POST.get('day')
        cost = request.POST.get('cost')
        if timeFrom == '' or timeTo == '' or cost == '':
            days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            data2 = {
                "day": days
            }
            return render(request, 'suggest_Package.html',data2)
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



