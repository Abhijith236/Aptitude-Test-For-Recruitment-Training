from django.shortcuts import render,redirect
from Admin.models import *
from Master.models import *
from User.models import *
from random import sample
from django.utils import timezone
import pytz
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from datetime import datetime

your_timezone = pytz.timezone('Asia/Kolkata')
current_datetime = timezone.localtime(timezone.now(), timezone=your_timezone)

current_date = current_datetime.date()  
current_time = current_datetime.time() 

def HomePage(request):
    return render(request,'User/HomePage.html')


def Category(request):
    categories = tbl_category.objects.all()
    return render(request, 'User/Category.html', {'categories': categories})


def Questions(request, cid):
    if 'uid' not in request.session:
        return redirect('login')  

    user_id = request.session['uid']
    user = tbl_user.objects.get(user_id=user_id)
    all_questions = tbl_question.objects.filter(category_id=cid)

    if all_questions.count() > 30:
        random_questions = sample(list(all_questions), 30)
    else:
        random_questions = all_questions

    if request.method == "POST":
        test = tbl_test.objects.get(user_id=user, test_status='0')
        test.test_end_time = timezone.now()
        test.test_status = '1'

        total_score = 0 

        for question in random_questions:
            answer_key = f'answer_{question.question_id}'
            user_answer = request.POST.get(answer_key)

            if user_answer == question.answer:
                total_score += question.question_score

            test_question = tbl_test_question.objects.create(
                test_id=test,
                test_question_answer=user_answer,
                test_question_score=question.question_score if user_answer == question.answer else 0,
                question_id=question  # Insert question_id into tbl_test_question
            )
            test_question.save()

        test.test_score = total_score
        test.save()

        return render(request, 'User/HomePage.html')
    else:
        data = tbl_test.objects.filter(user_id=request.session['uid'],test_status=0).count()
        if data > 0:
            return render(request, 'User/Questions.html', {'Questions': random_questions})
        else:
            test = tbl_test.objects.create(user_id=user)
            return render(request, 'User/Questions.html', {'Questions': random_questions})

def Test(request):
    if 'uid' not in request.session:
        return redirect('login')  

    user_id = request.session['uid']
    user = tbl_user.objects.get(user_id=user_id)
    all_questions = tbl_question.objects.all()

    if all_questions.count() > 30:
        random_questions = sample(list(all_questions), 30)
    else:
        random_questions = all_questions

    if request.method == "POST":
        test = tbl_test.objects.get(user_id=user, test_status='0')
        test.test_end_time = timezone.now()
        test.test_status = '1'

        total_score = 0 

        for question in random_questions:
            answer_key = f'answer_{question.question_id}'
            user_answer = request.POST.get(answer_key)

            if user_answer == question.answer:
                total_score += question.question_score

            test_question = tbl_test_question.objects.create(
                test_id=test,
                test_question_answer=user_answer,
                test_question_score=question.question_score if user_answer == question.answer else 0,
                question_id=question  # Insert question_id into tbl_test_question
            )
            test_question.save()

        test.test_score = total_score
        test.save()

        return render(request, 'User/HomePage.html')
    else:
        data = tbl_test.objects.filter(user_id=request.session['uid'],test_status=0).count()
        if data > 0:
            return render(request, 'User/Questions.html', {'Questions': random_questions})
        else:
            test = tbl_test.objects.create(user_id=user)
            return render(request, 'User/Questions.html', {'Questions': random_questions})


def PreviousTest(request):
    count = tbl_test.objects.filter(test_status='1', user_id=request.session['uid']).count()
    mae =0
    attended_tests=[]
    if count>0:
        attended_tests = tbl_test.objects.filter(test_status='1', user_id=request.session['uid'])
        # Fetch data from tbl_test
        tests = tbl_test.objects.filter(user_id=request.session['uid']).values('test_date', 'test_score')
        
        # Feature Engineering
        for test in tests:
            # Convert test_date to timestamp
            test['test_date'] = datetime.combine(test['test_date'], datetime.min.time()).timestamp()
        
        # Create DataFrame from the queryset
        import pandas as pd
        df = pd.DataFrame(list(tests))
        
        # Define features (X) and target variable (y)
        X = df[['test_date']]  # Feature: test_date
        y = df['test_score']  # Target variable: test_score
        
        # Initialize the Random Forest Regressor
        model = RandomForestRegressor()
        
        # Train the model (using the entire dataset as there's no split)
        model.fit(X, y)
        
        # Make predictions
        y_pred = model.predict(X)
        
        # Evaluate the model (using the entire dataset as there's no split)
        mae = mean_absolute_error(y, y_pred)
        
    # Pass the results to the template
    return render(request, 'User/PreviousTest.html', {'mae': mae,'attended_tests': attended_tests})

def TestQuestions(request, tid):
    attended_questions = tbl_test_question.objects.filter(test_id=tid)
    return render(request, 'User/TestQuestions.html', {'Questions': attended_questions})


def Logout(request):
    del request.session["uid"]
    return redirect("guest:Login")