from django.urls import path
from django.urls import re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name="authors"),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name="author-detail"),
]
# 個人借閱書籍
urlpatterns += [
    path('mybooks/', views.LoanedBookByUserListView.as_view(), name='my-borrowed')
]
# 所有借閱書籍
urlpatterns += [
    path('borrowed/', views.OnlyStaffViewUserBorrowed.as_view(), name='all-borrowed')
]
# 管理員延遲借書
urlpatterns += [
    path('borrowed/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]
# 民眾延遲借書
urlpatterns += [
    path('borrowed/<uuid:pk>/people-renew/', views.renew_book_people, name='renew-book-people'),
]
# 新增作者
urlpatterns += [
    path('author/create', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]
#新增書籍
urlpatterns +=[
    path('book/create',views.BookCreate.as_view(),name='book-create'),
]