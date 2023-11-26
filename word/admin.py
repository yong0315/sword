from django.contrib import admin
from .models import Voca_Book, Word

class VocaBookAdmin(admin.ModelAdmin):
    search_fields = ['title']

class WordListAdmin(admin.ModelAdmin):
    search_fields = ['content']

admin.site.register(Voca_Book, VocaBookAdmin)
admin.site.register(Word, WordListAdmin)