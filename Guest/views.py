from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *

def HomePage(requset):
    return render(requset,'Guest/HomePage.html')

def UserRegistration(request):
    district = tbl_district.objects.all()
    if request.method == "POST" and request.FILES:
        place = tbl_place.objects.get(place_id=request.POST.get("sel_place"))
        tbl_user.objects.create(
            user_name=request.POST.get('txt_name'),
            user_contact=request.POST.get('txt_contact'),
            user_email=request.POST.get('txt_email'),     
            user_proof=request.FILES.get('file_proof'),
            user_photo=request.FILES.get('file_photo'),
            user_address=request.POST.get('txt_address'),
            user_password=request.POST.get('txt_password'),
            place_id=place,
        )
        return render(request, "Guest/UserRegistration.html", {"district" : district})
    else:
        return render(request, "Guest/UserRegistration.html", {"district" : district})

def Login(request):
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        AdminCount =  tbl_admin.objects.filter(admin_email=email,admin_password=password).count()
        UserCount =  tbl_user.objects.filter(user_email=email,user_password=password).count()
        MasterCount =  tbl_master.objects.filter(master_email=email,master_password=password).count()
        if AdminCount > 0:
            admin = tbl_admin.objects.get(admin_email=email,admin_password=password)
            request.session["aid"] = admin.admin_id
            return redirect("admin:HomePage")
        elif MasterCount > 0:
            master = tbl_master.objects.get(master_email=email,master_password=password)
            request.session["mid"] = master.master_id
            return redirect("master:HomePage")  
        elif UserCount > 0:
            user = tbl_user.objects.get(user_email=email,user_password=password)
            request.session["uid"] = user.user_id
            return redirect("user:HomePage")
        else:
            return render(request,"Guest/Login.html",{"msg":"Invalid Email Or Password"})
    else:
        return render(request,"Guest/Login.html")