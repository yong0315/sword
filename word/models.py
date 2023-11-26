from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

class Voca_Book(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voca_book_list')
    title = models.CharField(max_length=50)
    view = models.IntegerField(default=0)
    voter = models.ManyToManyField(User, related_name='voca_book_voter')
    from_lang = models.CharField(max_length=50, default='en-US')
    to_lang = models.CharField(max_length=50, default='ko-KR')
    create_date = models.DateTimeField(null=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    is_share = models.BooleanField(default=True)

class Word(models.Model):
    voca_book = models.ForeignKey(Voca_Book, on_delete=models.CASCADE)
    voter = models.ManyToManyField(User, related_name='word_voter')
    content = models.TextField(null=True)
    mean = models.TextField(null=True)