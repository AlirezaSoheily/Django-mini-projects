from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('ask_question/', views.AskQuestion.as_view(), name='ask question'),
    path('answer/', views.AnswerQuestion.as_view(), name='answer'),
    path('questions/', views.Questions.as_view(), name='questions'),
    path('users_wq/', views.users_with_questions, name='users wq'),
    path('users_wma/', views.most_answers, name='most answers'),
    path('q_answers-<int:id>/', views.question_answers, name='question answers'),
    path('q_answers-<int:id>-<int:page_id>/', views.question_with_answers, name='question with answers'),
    path('2-answers/', views.question_2_answers, name='question 2 answers'),
    path('edit-<int:id>/', views.EditQuestion.as_view(), name='edit question'),
    path('search/', views.search, name='search'),

]
