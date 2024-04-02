from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *

def HomePage(requset):
    return render(requset,'Admin/HomePage.html')


# Category Function Start

def NewCategory(request):
    category = tbl_category.objects.all()
    if request.method=="POST":
        tbl_category.objects.create(category_name=request.POST.get('txt_category'))
        return render(request,"Admin/Category.html",{'category':category})
    else:
        return render(request,"Admin/Category.html",{'category':category})
    
def DeleteCategory(request,did):
    tbl_category.objects.get(category_id=did).delete()
    return redirect("admin:NewCategory")

def EditCategory(request,eid):
    category = tbl_category.objects.all()
    editdata=tbl_category.objects.get(category_id=eid)
    if request.method=="POST":
        editdata.category_name=request.POST.get('txt_category')
        editdata.save()
        return redirect("admin:NewCategory")
    else:
        return render(request,"Admin/Category.html",{'editdata':editdata,'category':category})
    
# Category Functions End


# District Function Start

def NewDistrict(request):
    district = tbl_district.objects.all()
    if request.method=="POST":
        tbl_district.objects.create(district_name=request.POST.get('txt_district'))
        return render(request,"Admin/District.html",{'district':district})
    else:
        return render(request,"Admin/District.html",{'district':district})
    
def DeleteDistrict(request,did):
    tbl_district.objects.get(district_id=did).delete()
    return redirect("admin:NewDistrict")

def EditDistrict(request,eid):
    district = tbl_district.objects.all()
    editdata=tbl_district.objects.get(district_id=eid)
    if request.method=="POST":
        editdata.district_name=request.POST.get('txt_district')
        editdata.save()
        return redirect("admin:NewDistrict")
    else:
        return render(request,"Admin/District.html",{'editdata':editdata,'district':district})
    
# District Functions End
    

# Place functions Start
    
def NewPlace(request):
    place=tbl_place.objects.all()
    district=tbl_district.objects.all()
    if request.method=="POST":
        selectedState=tbl_district.objects.get(district_id=request.POST.get('sel_district'))
        tbl_place.objects.create(place_name=request.POST.get("txt_place"),district_id=selectedState)
        return render(request,"Admin/Place.html",{'district':district,'place':place})
    else:
        return render(request,"Admin/Place.html",{'district':district,'place':place})
    
def DeletePlace(request,did):
    tbl_place.objects.get(place_id=did).delete()
    return redirect("admin:NewPlace")


def EditPlace(request,eid):
    district=tbl_district.objects.all()
    place = tbl_place.objects.all()
    editdata=tbl_place.objects.get(place_id=eid)
    if request.method=="POST":
        editdata.place_name=request.POST.get('txt_place')
        editdata.district_id=tbl_district.objects.get(district_id=request.POST.get('sel_district'))
        editdata.save()
        return redirect("admin:NewPlace")
    else:
        return render(request,"Admin/Place.html",{'editdata':editdata,'place':place,'district':district})

# Place functions End
    

def Master(request):
    master = tbl_master.objects.all()
    if request.method == "POST" and request.FILES:
        tbl_master.objects.create(
            master_name=request.POST.get('txt_name'),
            master_contact=request.POST.get('txt_contact'),
            master_email=request.POST.get('txt_email'),
            master_photo=request.FILES.get('file_photo'),
            master_password=request.POST.get('txt_password'),
        )
        return render(request, "Admin/Master.html", {"master" : master})
    else:
        return render(request, "Admin/Master.html", {"master" : master})
    
def DeleteMaster(request,mid):
    tbl_master.objects.get(master_id=mid).delete()
    return redirect("admin:Master")

def AjaxPlace(request):
    district=tbl_district.objects.get(district_id=request.GET.get("did"))
    place=tbl_place.objects.filter(district_id=district)
    return render(request,"Admin/AjaxPlace.html",{"place" : place})
    
def Logout(request):
    del request.session["aid"]
    return redirect("guest:Login")