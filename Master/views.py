from django.shortcuts import render,redirect
from Admin.models import *
from Master.models import *

def HomePage(requset):
    return render(requset,'Master/HomePage.html')

def Questions(request):
    category = tbl_category.objects.all()
    if request.method == "POST":
        selectedCategory = tbl_category.objects.get(category_id=request.POST.get("sel_category"))
        tbl_question.objects.create(
            question_content=request.POST.get('txt_question_content'),
            question_score=request.POST.get('txt_question_score'),
            option_1=request.POST.get('txt_option1'),     
            option_2=request.POST.get('txt_option2'),     
            option_3=request.POST.get('txt_option3'),
            option_4=request.POST.get('txt_option4'),
            answer=request.POST.get('txt_answer'),
            answer_key=request.POST.get('txt_answer_key'),
            category_id=selectedCategory,
        )
        return render(request, "Master/Questions.html", {"category" : category})
    else:
        return render(request, "Master/Questions.html", {"category" : category})
    

def Logout(request):
    del request.session["mid"]
    return redirect("guest:Login")