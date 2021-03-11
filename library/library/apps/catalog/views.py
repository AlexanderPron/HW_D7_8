from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Book, PublishingHouse, BookInUse, Friend
from catalog.forms import BookForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView
from django.template import loader
from django.shortcuts import redirect

def books_list(request):
    books = Book.objects.all()
    return HttpResponse(books)

def index(request):
    template = loader.get_template('index.html')
    books = Book.objects.all()
    biblio_data = {
        "title": "мою библиотеку",
        "books": books,
    }
    
    return HttpResponse(template.render(biblio_data, request))

def book_increment(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/')
            book.copy_count += 1
            book.save()
        return redirect('/')
    else:
        return redirect('/')


def book_decrement(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/')
            if book.copy_count < 1:
                book.copy_count = 0
            else:
                book.copy_count -= 1
            book.save()
        return redirect('/')
    else:
        return redirect('/')

def ph(request):
    template = loader.get_template('publishing_house.html')
    ph_list = PublishingHouse.objects.all()
    data = {
        "ph_list": ph_list,
    }
    return HttpResponse(template.render(data, request))

def bk(request):
    template = loader.get_template('book_keeping.html')
    bk_list = BookInUse.objects.all()
    
    data = {
        "bk_list": bk_list,
    }
    return HttpResponse(template.render(data, request))

# class BookEdit(UpdateView):  
#     model = Book  
#     form_class = BookForm  
#     success_url = reverse_lazy('index')  
#     template_name = 'update_book.html'  

def book_add(request):
    form = BookForm(request.POST or None)
    if request.method == 'POST':
        if 'create_single' in request.POST:
            if form.is_valid():
                book = form.save()
                book.book_img = request.FILES['book_img']
                book.save()
                return HttpResponseRedirect(reverse_lazy('index'))
        elif 'create_and_add' in request.POST:
            if form.is_valid():
                book = form.save()
                book.book_img = request.FILES['book_img']
                book.save()
                return HttpResponseRedirect(reverse_lazy('add-book'))
    return render(request, 'add_book.html', {'form': form})
