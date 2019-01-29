import datetime

from django.shortcuts import render

from centers.models import Center, Discounts
from reviews.models import StarRating


def centerRate(request):
    if request.method == 'POST':
        centerId = request.POST.get("details")
        innercenter = Center.objects.get(id=centerId)
        userId = request.user
        userRate = request.POST.get("rating")
        if userRate != None:
            sc = StarRating.objects.filter(user_id=userId,center_id=innercenter)
            if sc.count() > 0 :
                StarRating.objects.filter(user_id_id=userId,center_id=innercenter).update(rate=userRate)
            else:
                d, form = StarRating.objects.get_or_create(center_id=innercenter, user_id=userId, rate=int(userRate))
                d.save()



    flag=None
    #centerDiscount=Discounts.objects.filter(center_id=centerId)
    if Discounts.objects.filter(center_id=centerId).count() > 0 :
        centerDiscount = Discounts.objects.filter(center_id=centerId)
        for a in centerDiscount:
            if a.expiration_date >= datetime.date.today():
                flag=a.new_cost
                centers=Center.objects.filter(id=centerId)
                for l in centers:
                    if l.ticket_cost == flag:
                        flag=None

    stars_5 = StarRating.objects.filter(rate=5,center_id=centerId).count()
    stars_4 = StarRating.objects.filter(rate=4,center_id=centerId).count()
    stars_3 = StarRating.objects.filter(rate=3,center_id=centerId).count()
    stars_2 = StarRating.objects.filter(rate=2,center_id=centerId).count()
    stars_1 = StarRating.objects.filter(rate=1,center_id=centerId).count()
    sum=(stars_5 + stars_4 + stars_3 + stars_2 + stars_1)
    if sum != 0 :
     avg_5 = (stars_5 * 100) / sum
     avg_4 = (stars_4 * 100) / sum
     avg_3 = (stars_3 * 100) / sum
     avg_2 = (stars_2 * 100) / sum
     avg_1 = (stars_1 * 100) / sum
     avg_all=((5*stars_5)+(4*stars_4)+(3*stars_3)+(2*stars_2)+(1*stars_1))/sum
    else:
        avg_5 = 0
        avg_4 = 0
        avg_3 = 0
        avg_2 = 0
        avg_1 = 0
        avg_all = 0
    numOfRev = stars_5 + stars_4 + stars_3 + stars_2 + stars_1
    data={
        "xx":centerId,
        'centerInfo':Center.objects.get(id=centerId),
        'centerDis':flag,
        'stars_5': stars_5,
        'stars_4': stars_4,
        'stars_3': stars_3,
        'stars_2': stars_2,
        'stars_1': stars_1,
        'avg_5': avg_5,
        'avg_4': avg_4,
        'avg_3': avg_3,
        'avg_2': avg_2,
        'avg_1': avg_1,
        'all':numOfRev,
        'avg_all': avg_all,

    }
    return render(request, 'center_actions_and_details.html',data)




