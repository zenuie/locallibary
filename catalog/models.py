# class MyModelName(models.Model):
#     """定義模型的典型，該類源自於Model class。"""
#     # Fields -字段
#     my_field_name = models.CharField(max_length=20, help_text='Enter field documentation')
#     '''
#     max_length=20 — 表示此字段中值的最大長度為20個字符的狀態。
#     help_text="Enter field documentation" — 提供一個幫助用戶的文本標籤，讓用戶知道當前透過HTML表單輸入時要提供什麼值。
#     '''
#
#     # Metadata -元數據 與資料相關的資料
#     class Meta:
#         """元數據最有用的功能之一是控制在查詢模型類型時返回之記錄的預設排序"""
#         ordering = ['-my_field_name']
#
#     # Methods -模式
#     def get_absolute_url(self):
#         """返回url讀取MyModelName內特定的資訊"""
#         return reverse('model-detail-view', args=[str(self.id)])
#
#     '''
#     最起碼，在每個模型中，你應該定義標準的Python 類方法__str__() ，來為每個物件返回一個人類可讀的字符串
#     '''
#
#     def __str__(self):
#         """代表MyModelName字串"""
#         return self.my_field_name
#
#
# """創建和修改記錄"""
# # 建立模組紀錄
# record = MyModelName(my_field_name="Instance #1")
#
# # 儲存模組紀錄
# record.save()
#
# # Access model field values using Python attributes.
# print(record.id)  # 應該會成為第一條回傳 返回1
# print(record.my_field_name)  # 會回傳Instance #1
#
# # 通過修改字段，然後調用save（）來更改記錄。.
# record.my_field_name = "New Instance Name"
# record.save()
#
# """搜尋紀錄"""
# all_books = Book.objects.all()
# wild_books = Book.objects.filter(title__contains='wild')
# number_wild_books = Book.objects.filter(title__contains='wild').count()
# # 會比對到: Fiction, Science fiction, non-fiction etc.
#
#
# books_containing_genre = Book.objects.filter(genre__name__icontains='fiction')

"""定義local library模型"""
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

import uuid


# Create your models here

# 書籍類型模組
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Eenter a book genre (e.g Science Fiction')

    def __str__(self):
        return self.name


# 書本模組
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    def display_genre(self):
        '''Create a string for the Genre. This is required to display genre in Admin.'''
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


# 書本語言模組
class Language(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        return self.name


# 書本詳情模組
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id}({self.book.title})'


# 作者模組
class Author(models.Model):
    first_name = models.CharField('名字',max_length=100)
    last_name = models.CharField('姓氏',max_length=100)
    data_of_birth = models.DateField('出生',null=True, blank=True)
    data_of_death = models.DateField('逝世', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name},{self.first_name}'



