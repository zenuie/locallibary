from django.http import Http404
from django.shortcuts import render

# Create your views here.
from .models import Book, Author, BookInstance, Genre, Language
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


@login_required
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


class OnlyStaffViewUserBorrowed(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'bookinstance_list_all_user_borrowed.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
