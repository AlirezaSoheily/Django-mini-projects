from django.shortcuts import render, HttpResponse
from django.views import View
from .models import User, Question, Answers, QuestionManager
from django.views.generic import ListView
from django.db.models import Count, Q
from django.core.paginator import Paginator


class Register(View):
    def get(self, request):
        return render(request, 'Register.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        user = User(username=username, password=password, name=name, email=email)
        user.save()
        return HttpResponse("Registered!")


class AskQuestion(View):
    def get(self, request):
        users = User.objects.all()
        context = {'users': users}
        return render(request, 'Question.html', context)

    def post(self, request):
        title = request.POST['title']
        body = request.POST['body']
        u = request.POST['users']
        user = User.objects.get(id=u)
        question = Question(user_id=user, title=title, body=body)
        question.save()
        return HttpResponse('Question submitted!')


class AnswerQuestion(View):
    def get(self, request):
        users = User.objects.all()
        questions = Question.objects.all()
        context = {'users': users, 'questions': questions}
        return render(request, 'answer.html', context)

    def post(self, request):
        body = request.POST['body']
        u = request.POST['users']
        user = User.objects.get(id=u)
        q = request.POST['questions']
        question = Question.objects.get(id=q)
        answer = Answers(user_id=user, body=body, question_id=question)
        answer.save()
        return HttpResponse('Answer submitted!')


class Questions(ListView):
    model = Question
    template_name = 'Question list.html'


def users_with_questions(request):
    users = Question.objects.values('user_id_id__name')
    return render(request, 'Users with questions.html', {'users': list(users)})


def most_answers(request):
    users = Answers.objects.values('user_id_id__name').annotate(total=Count('user_id_id')).order_by('-total')
    return render(request, 'Users with most question.html', {'users': list(users)})


def question_answers(request, id):
    question = Question.objects.get(id=id)
    answers = Answers.objects.filter(question_id=id)
    return render(request, 'question answers.html', {'question': question, 'answers': list(answers)})


def question_with_answers(request, id, page_id):
    question = Question.objects.get(id=id)
    answers = Answers.objects.filter(question_id=id)
    paginator = Paginator(answers, 3)
    page_obj = paginator.get_page(page_id)
    return render(request, 'Question With Answers.html', {'question': question, 'answers': page_obj})


def question_2_answers(request):
    questions = Question.objects.questions_with_2_answers()
    return render(request, 'Question with 2 answers.html', {'questions': questions})


class EditQuestion(View):
    def get(self, request, id):
        question = Question.objects.get(id=id)
        return render(request, 'Edit question.html', {'question': question})

    def post(self, request, id):
        question = Question.objects.get(id=id)
        if request.POST['delete'] == 'delete':
            question.delete()
            return HttpResponse('Question deleted!')
        title = request.POST['title']
        body = request.POST['body']
        question.title = title
        question.body = body
        question.save()
        return HttpResponse('Edit saved!')


def search(request):

    if request.method == "GET":
        query = request.GET.get('search')

        if query == '':
            query = 'None'

        questions = Question.objects.filter(Q(body__icontains=query))
        answers = Answers.objects.filter(Q(body__icontains=query))

    return render(request, 'Search.html', {'questions': questions, 'answers': answers})
