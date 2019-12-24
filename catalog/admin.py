from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language

# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)
admin.site.site_header = "書本管理登入"


class BookInline(admin.TabularInline):
    # pass
    model = Book


# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    # pass
    list_display = ('last_name', 'first_name', 'data_of_birth', 'data_of_death')
    fields = ['first_name', 'last_name', ('data_of_birth', 'data_of_death')]
    inlines = [BookInline]


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    # pass
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )


class BookInstanceInline(admin.TabularInline):
    # pass
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # pass
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]
