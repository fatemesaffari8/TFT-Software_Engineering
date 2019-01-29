from django.shortcuts import render

from interests.models import Interest
from users.models import UserInterests


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


