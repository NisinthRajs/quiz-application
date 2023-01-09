# from django.shortcuts import redirect,render
# from django.contrib.auth import login,logout,authenticate
# from .forms import *
# from .models import *
# from django.http import HttpResponse
# from random import randint
# from django.core.paginator import Paginator

# # Create your views here.
# def home(request):
    
#     questions = QuesModel.objects.all()
#     paginator = Paginator(questions,1)
#     page_number = request.GET.get('page')
#     page_obj = Paginator.get_page(paginator, page_number)
#     context = {'questions': questions, 'page_obj': page_obj,}
    

#     if request.method == 'GET':
#         request.session['previous_page'] = request.path_info + "?page=" + request.GET.get("page", '1')
#         return render(request, 'Quiz/home.html', context)
    
#     if request.method == 'POST':
#         print(request.POST)
#         score=0
#         wrong=0
#         correct=0
#         total=0
#         for q in questions:
#             total+=1
#             print(request.POST.get(q.question))
#             print(q.ans)
#             print()
#             if q.ans ==  request.POST.get(q.question):
#                 score+=10
#                 correct+=1
#             else:
#                 wrong+=1
#         percent = score/(total*10) *100
#         context = {
#             'score':score,
#             'time': request.POST.get('timer'),
#             'correct':correct,
#             'wrong':wrong,
#             'percent':percent,
#             'total':total
#         }
#         return render(request,'Quiz/result.html',context)
#     else:
#         questions=QuesModel.objects.all()
#         context = {
#             'questions':questions
#         }
#         return render(request,'Quiz/home.html',context)

# def addQuestion(request):    
#     if request.user.is_staff:
#         form=addQuestionform()
#         if(request.method=='POST'):
#             form=addQuestionform(request.POST)
#             if(form.is_valid()):
#                 form.save()
#                 return redirect('/')
#         context={'form':form}
#         return render(request,'Quiz/addQuestion.html',context)
#     else: 
#         return redirect('home') 

# def registerPage(request):
#     if request.user.is_authenticated:
#         return redirect('home') 
#     else: 
#         form=createuserform()
#         if request.method=='POST':
#             form=createuserform(request.POST)
#             if form.is_valid() :
#                 user=form.save()
#                 return redirect('login')
#         context={
#             'form':form,
#         }
#         return render(request,'Quiz/register.html',context)

# def loginPage(request):
#     if request.user.is_authenticated:
#         return redirect('home')
#     else:
#        if request.method=="POST":
#         username=request.POST.get('username')
#         password=request.POST.get('password')
#         user=authenticate(request,username=username,password=password)
#         if user is not None:
#             login(request,user)
#             #messages.success(request, 'You have successfully logged in')
#             return redirect('/')
#         else:
#             #messages.success(request, 'Error logging in')
#             return redirect('login')
#        context={}
#        return render(request,'Quiz/login.html',context)

# def logoutPage(request):
#     logout(request)
#     return redirect('/')


from django.shortcuts import render, redirect
from .models import Category, Question
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/login/')
def index_page(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'index.html', context)

@login_required(login_url='/login/')
def take_quiz(request, pk):
    questions = Question.objects.filter(choice=pk).order_by('-created_at')
    paginator = Paginator(questions,1)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {'questions': questions, 'page_obj': page_obj,}
    

    if request.method == 'GET':
        request.session['previous_page'] = request.path_info + "?page=" + request.GET.get("page", '1')
        return render(request, 'quiz.html', context)
    
    if request.method == 'POST':
        correct_user_answers = []
        user_answer = request.POST['option']
        correct_answer = request.POST.get('answerLabel')
        print('correct answer ',correct_answer)
        print('user answer: ', user_answer)
        if user_answer == correct_answer:
            correct_user_answers.append(user_answer)
            messages.success(request, 'Correct answer')
            return HttpResponseRedirect(request.session['previous_page'])
        else:
            messages.warning(request, f'Wrong answer, Correct Answer is {correct_answer}')
            return HttpResponseRedirect(request.session['previous_page'])