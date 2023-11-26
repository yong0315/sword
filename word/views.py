from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.utils import timezone, dateformat
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Voca_Book, Word
from .forms import VocaBookForm, WordForm

def index(request):
    page = request.GET.get('page', '1')
    type = request.GET.get('type', 'all')
    kw = request.GET.get('kw', '')
    
    voca_book_list = Voca_Book.objects.filter(
        Q(is_share=True)
    ).order_by('-create_date')
    if request.user.is_authenticated:
        voca_book_mine = Voca_Book.objects.filter(
            Q(author__username__icontains=request.user.username)
        ).order_by('-create_date')
        voca_book_like = Voca_Book.objects.filter(
            Q(is_share=True) &
            Q(voter__username__icontains=request.user.username)
        ).order_by('-create_date')
    else:
        voca_book_mine = []
        voca_book_like = []
    
    if kw:
        if type == 'all':
            voca_book_list = voca_book_list.filter(
                Q(title__icontains=kw) |
                Q(author__username__icontains=kw)  # 질문 글쓴이 검색
            ).distinct()
        elif type == 'mine':
            voca_book_mine = voca_book_mine.filter(
                Q(title__icontains=kw) |
                Q(author__username__icontains=kw)  # 질문 글쓴이 검색
            ).distinct()
        elif type == 'like':
            voca_book_like = voca_book_like.filter(
                Q(title__icontains=kw) |
                Q(author__username__icontains=kw)
            ).distinct()
    
    paginator_all = Paginator(voca_book_list, 10)
    paginator_mine = Paginator(voca_book_mine, 10)
    paginator_like = Paginator(voca_book_like, 10)
    
    page_obj_all = paginator_all.get_page(page if type == 'all' else 1)
    page_obj_mine = paginator_mine.get_page(page if type == 'mine' else 1)
    page_obj_like = paginator_like.get_page(page if type == 'like' else 1)
    context = {'voca_book_list': page_obj_all, 'voca_book_mine': page_obj_mine, \
            'voca_book_like': page_obj_like, 'type': type, 'page': page, 'kw': kw}
    return render(request, 'word/voca_book_list.html', context)

def detail(request, voca_id):
    voca_book = get_object_or_404(Voca_Book, pk=voca_id)
    word_list = voca_book.word_set.all()
    word_mark = Word.objects.filter(
            Q(voca_book__id=voca_id) &
            Q(voter__username__icontains=request.user.username)
        )
    context = {'voca_book': voca_book, 'word_list': word_list, 'word_mark': word_mark}
    voca_book.view += 1
    voca_book.save()
    return render(request, 'word/word_list.html', context)

@login_required(login_url='common:login')
def voca_book_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        if request.POST['is_share'] == 'open': is_share = True
        elif request.POST['is_share'] == 'close': is_share = False
        from_lang = request.POST['from_lang']
        to_lang = request.POST['to_lang']
        
        form = VocaBookForm({'title': title, 'is_share': is_share, \
                            'from_lang': from_lang, 'to_lang': to_lang})
        if form.is_valid():
            voca_book = form.save(commit=False)
            voca_book.author = request.user
            voca_book.create_date = timezone.now()
            voca_book.save()
            return redirect('sword:index')
    else:
        form = VocaBookForm()
    context = {'form': form}
    return render(request, 'word/voca_book_form.html', context)

@login_required(login_url='common:login')
def voca_book_modify(request, voca_id):
    voca_book = get_object_or_404(Voca_Book, pk=voca_id)
    if request.user != voca_book.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('sword:detail', voca_id=voca_book.id)
    if request.method == "POST":
        title = request.POST['title']
        if request.POST['is_share'] == 'open': is_share = True
        elif request.POST['is_share'] == 'close': is_share = False
        from_lang = request.POST['from_lang']
        to_lang = request.POST['to_lang']
        
        form = VocaBookForm({'title': title, 'is_share': is_share, \
                            'from_lang': from_lang, 'to_lang': to_lang}, instance=voca_book)
        if form.is_valid():
            voca_book = form.save(commit=False)
            voca_book.modify_date = timezone.now()
            voca_book.save()
            return redirect('sword:detail', voca_id=voca_book.id)
    else:
        form = VocaBookForm(instance=voca_book)
    context = {'form': form}
    return render(request, 'word/voca_book_form.html', context)

@login_required(login_url='common:login')
def words_modify(request, voca_id):
    voca_book = get_object_or_404(Voca_Book, pk=voca_id)
    if request.user != voca_book.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('sword:detail', voca_id=voca_book.id)
    if request.method == "POST":
        new_words = []
        leng = len(request.POST.getlist('content'))
        words = voca_book.word_set.all()
        for i in range(leng):
            content = request.POST.getlist('content')[i]
            mean = request.POST.getlist('mean')[i]
            new_word = {'content': content, 'mean': mean}
            form = WordForm({'content': content, 'mean': mean})
            if form.is_valid():
                new_words.append(new_word)
        idx = 0
        for word in words:
            if idx < len(new_words):
                form = WordForm(new_words[idx], instance=word)
                form.save()
                idx += 1
            else:
                temp = word
                temp.delete()
        if len(new_words) > len(words):
            for i in range(idx, len(new_words)):
                form = WordForm(new_words[i])
                word = form.save(commit=False)
                word.voca_book = voca_book
                word.save()
        voca_book.modify_date = timezone.now()
        voca_book.save()
        return redirect('sword:detail', voca_id=voca_book.id)
    else:
        word_forms = []
        for word in voca_book.word_set.all():
            form = WordForm(instance=word)
            word_forms.append(form)
    context = {'voca_book': voca_book, 'forms': word_forms}
    return render(request, 'word/word_form.html', context)

@login_required(login_url='common:login')
def voca_book_delete(request, voca_id):
    voca_book = get_object_or_404(Voca_Book, pk=voca_id)
    if request.user != voca_book.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('sword:detail', voca_id=voca_book.id)
    voca_book.delete()
    return redirect('sword:index')

@login_required(login_url='common:login')
def voca_book_vote(request, voca_id):
    voca_book = get_object_or_404(Voca_Book, pk=voca_id)
    voca_book.voter.add(request.user)
    return redirect('sword:index')

@login_required(login_url='common:login')
def voca_vote_cancel(request, voca_id):
    voca_book = get_object_or_404(Voca_Book, pk=voca_id)
    voca_book.voter.remove(request.user)
    return redirect('sword:index')   

@login_required(login_url='common:login')
def word_vote(request, word_id):
    word = get_object_or_404(Word, pk=word_id)
    word.voter.add(request.user)
    word.voca_book.view -= 1
    word.voca_book.save()
    return redirect('sword:detail', voca_id=word.voca_book.id)

@login_required(login_url='common:login')
def word_vote_cancel(request, word_id):
    word = get_object_or_404(Word, pk=word_id)
    word.voter.remove(request.user)
    word.voca_book.view -= 1
    word.voca_book.save()
    return redirect('sword:detail', voca_id=word.voca_book.id)