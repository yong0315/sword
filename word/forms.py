from django import forms
from word.models import Voca_Book, Word

class VocaBookForm(forms.ModelForm):
    class Meta:
        model = Voca_Book
        fields = ['title', 'is_share', 'from_lang', 'to_lang']
        labels = {
            'title': '이름',
            'is_share': '공개 여부',
            'from_lang': '시작 언어',
            'to_lang': '도착 언어',
        }

class WordForm(forms.ModelForm):
    class Meta:
        model = Word  # 사용할 모델
        fields = ['content', 'mean']
        labels = {
            'content': '단어',
            'mean': '의미',
        }