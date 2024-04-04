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
        return redirect("user:TestQuestions",test.id)
    else:
        data = tbl_test.objects.filter(user_id=request.session['uid'],test_status=0).count()
        if data > 0:
            return render(request, 'User/Questions.html', {'Questions': random_questions})
        else:
            test = tbl_test.objects.create(user_id=user)
            return render(request, 'User/Questions.html', {'Questions': random_questions})


def PreviousTest(request):
    """
    View function for displaying previous test information and calculating Mean Absolute Error (MAE).

    Parameters:
    - request: HttpRequest object containing metadata about the HTTP request.

    Returns:
    - Rendered HTML template displaying previous test information and MAE.

    Algorithm:
    1. Query the database to count the number of tests associated with the user.
    2. If tests are found:
        a. Retrieve attended tests with status '1' for the user.
        b. Retrieve all tests (regardless of status) for the user, selecting 'test_date' and 'test_score' fields.
        c. Convert 'test_date' field of each test to timestamp representation.
        d. Convert the queryset of tests into a pandas DataFrame.
        e. Define features (X) and target variable (y) for machine learning.
        f. Train a Random Forest Regressor model using the features and target variable.
        g. Make predictions using the trained model.
        h. Calculate Mean Absolute Error (MAE) between actual and predicted test scores.
    3. Render a template with the calculated MAE and attended test information.

    """
    # Count the number of tests associated with the user
    count = tbl_test.objects.filter(test_status='1', user_id=request.session['uid']).count()
    
    # Initialize variables for MAE and attended tests
    mae = 0
    attended_tests = []
    
    # If tests are found
    if count > 0:
        # Retrieve attended tests for the user
        attended_tests = tbl_test.objects.filter(test_status='1', user_id=request.session['uid'])
        
        # Retrieve all tests for the user, selecting 'test_date' and 'test_score' fields
        tests = tbl_test.objects.filter(user_id=request.session['uid']).values('test_date', 'test_score')
        
        # Convert 'test_date' field of each test to timestamp representation
        for test in tests:
            test['test_date'] = datetime.combine(test['test_date'], datetime.min.time()).timestamp()
        
        # Convert the queryset of tests into a pandas DataFrame
        import pandas as pd
        df = pd.DataFrame(list(tests))
        
        # Define features (X) and target variable (y) for machine learning
        X = df[['test_date']]  # Feature: test_date
        y = df['test_score']    # Target variable: test_score
        
        # Initialize Random Forest Regressor model
        model = RandomForestRegressor()
        
        # Train the model
        model.fit(X, y)
        
        # Make predictions
        y_pred = model.predict(X)
        
        # Calculate Mean Absolute Error (MAE)
        mae = mean_absolute_error(y, y_pred)
    
    # Render a template with MAE and attended test information
    return render(request, 'User/PreviousTest.html', {'mae': mae, 'attended_tests': attended_tests})

def TestQuestions(request, tid):
    attended_questions = tbl_test_question.objects.filter(test_id=tid)
    return render(request, 'User/TestQuestions.html', {'Questions': attended_questions})


def Logout(request):
    del request.session["uid"]
    return redirect("guest:Login")
