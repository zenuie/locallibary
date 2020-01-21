from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect

# Create your views here.
from .models import Book, Author, BookInstance, Genre, Language
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# 驗證模組
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from .forms import RenewBookForm


def index(request):
    '''
    View function for home page of site.
    '''

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available books(status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    num_language = Language.objects.count()

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,
                 'num_language': num_language, 'num_visits': num_visits}
    )


# 管理員裝飾器
def staff_required(func):
    def auth(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse('login'))
        return func(request, *args, **kwargs)

    return auth


def registered_people(func):
    def auth(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return func(request, *args, **kwargs)

    return auth


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.filter(title__icontains='')

    template_name = 'book_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Book
    template_name = 'book_detail.html'

    def book_detail_view(request, primary_key):
        try:
            book = Book.objects.get(pk=primary_key)
        except Book.DoesNotExist:
            raise Http404("Book does not exist")
        return render(
            request,
            'book_detail.html',
            context={'book': book}
        )


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    template_name = 'author_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Author
    template_name = 'author_detail.html'

    def author_detail_view(request, primary_key):
        try:
            author = Author.objects.get(pk=primary_key)
        except Author.DoesNotExist:
            raise Http404("Author does not exist")
        return render(
            request,
            'author_detail.html',
            context={'author': author}
        )


class LoanedBookByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class OnlyStaffViewUserBorrowed(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'bookinstance_list_all_user_borrowed.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@staff_required
def renew_book_librarian(request, pk):
    """
    讓館員用來更新書本具體資訊的功能
    """
    book_inst = get_object_or_404(BookInstance, pk=pk)
    # 如果送來的是POST請求，就處理表單數據
    if request.method == 'POST':
        # 給予表單內容
        form = RenewBookForm(request.POST)
        # 確認表單是否有效
        if form.is_valid():
            # 如果有效將其寫入due_back
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            # 轉址到新URL
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date, })
    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})

@registered_people
def renew_book_people(request, pk):
    """
    讓民眾用來更新書本具體資訊的功能
    """
    book_inst = get_object_or_404(BookInstance, pk=pk)
    # 如果送來的是POST請求，就處理表單數據
    if request.method == 'POST':
        # 給予表單內容
        form = RenewBookForm(request.POST)
        # 確認表單是否有效
        if form.is_valid():
            # 如果有效將其寫入due_back
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            # 轉址到新URL
            return HttpResponseRedirect(reverse('my-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date, })
    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})
