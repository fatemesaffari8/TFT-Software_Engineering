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
    return render(request,'userProfile.html',fav)

def choose_and_edit_interests(request):
    interests = Interest.objects.all()
    currentUser = request.user.id
    if request.method == 'POST':
        fav = request.POST.get("fav")
        intFav=int(fav)
        userInterests = UserInterests.objects.filter(user_id=currentUser)
        flag=0
        for a in userInterests:
            if a.interest_id == intFav:
                flag =1
        if flag == 1:
            UserInterests.objects.filter(user_id=currentUser, interest_id=intFav).delete()
            flag = 0
        else:
            new_entry = UserInterests(user_id=currentUser, interest_id=intFav)
            new_entry.save()

    currentUserInterests=UserInterests.objects.filter(user_id=currentUser)
    CUIds=[]
    for a in currentUserInterests:
        CUIds.append(a.interest_id)
    data={
            "interests":interests,
            "currentUserInterests":CUIds,
        }
    return render(request,'interest.html',data)


