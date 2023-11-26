from django.urls import path
from . import views

app_name = 'sword'

urlpatterns = [
    path('', views.index, name='index'),
    path('voca_book/<int:voca_id>', views.detail, name='detail'),
    path('voca_book/create/', views.voca_book_create, name='voca_book_create'),
    path('voca_book/modify/<int:voca_id>/', views.voca_book_modify, name='voca_book_modify'),
    path('voca_book/word/modify/<int:voca_id>/', views.words_modify, name='words_modify'),
    path('voca_book/delete/<int:voca_id>/', views.voca_book_delete, name='voca_book_delete'),
    path('voca_book/vote/<int:voca_id>/', views.voca_book_vote, name='voca_book_vote'),
    path('voca_book/vote/cancel/<int:voca_id>/', views.voca_vote_cancel, name='voca_vote_cancel'),
    path('voca_book/word/vote/<int:word_id>/', views.word_vote, name='word_vote'),
    path('voca_book/word/vote/cancel/<int:word_id>/', views.word_vote_cancel, name='word_vote_cancel'),
]