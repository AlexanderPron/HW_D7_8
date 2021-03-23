from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Book, PublishingHouse, BookInUse, Friend, UserProfile
from catalog.forms import BookForm, ProfileEditForm
from django.contrib.auth.forms import UserCreationForm  
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, DetailView
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from allauth.account.views import SignupView
from .models import UserProfile

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

class CreateUserProfile(LoginRequiredMixin, FormView):
    form_class = ProfileEditForm
    template_name = 'profile-edit.html'  
    success_url = reverse_lazy('index')

    # def dispatch(self, request, *args, **kwargs):  
    #     if self.request.user.is_anonymous:  
    #         return HttpResponseRedirect(reverse_lazy('login'))  
    #     return super(CreateUserProfile, self).dispatch(request, *args, **kwargs)  
  
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super(CreateUserProfile, self).form_valid(form)
    
    def get(self, request, *args, **kwargs):
        ctxt = {}
        if request.user.id != self.kwargs['pk']:
            ctxt['error_msg_no_rights'] = True
        return render(request, self.template_name, self.get_context_data(**ctxt))

class ShowUserProfile(LoginRequiredMixin, FormView):
    form_class = ProfileEditForm
    template_name = 'profile-show.html'

    def get_object(self):
        obj = None
        try:
            obj = UserProfile.objects.get(user__id=self.kwargs['pk'])
        except:
            pass
        return obj

    def get_context_data(self, **kwargs):
        curr_user = self.get_object()
        if curr_user:
            kwargs['curr_user'] = curr_user
            kwargs['user_form'] = ProfileEditForm(initial={'user':curr_user}, instance=kwargs['curr_user'])
        else:
            kwargs['error_msg_no_profile'] = True
        return kwargs

    def get(self, request, *args, **kwargs):
        ctxt = {}
        if request.user.id != self.kwargs['pk']:
            ctxt['error_msg_no_rights'] = True
        return render(request, self.template_name, self.get_context_data(**ctxt))

    def post(self, request, *args, **kwargs):
        user_form = ProfileEditForm(request.POST, instance=self.get_object())
        if user_form.is_valid():
            user_form.save()
        return render(request, self.template_name, self.get_context_data())
        