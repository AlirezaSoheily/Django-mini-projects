from django.db import models
from django.db.models import Count


class User(models.Model):
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)


class QuestionManager(models.Manager):
    def questions_with_2_answers(self):
        target = []
        answer = Answers.objects.values_list('question_id_id').annotate(
            total=Count('question_id_id')).distinct()
        for a in answer:
            if a[1] > 1:
                target.append(a[0])
        question = Question.objects.filter(id__in=target)
        return question


class Question(models.Model):
    objects = QuestionManager()
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=250)
    body = models.TextField()


class Answers(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
