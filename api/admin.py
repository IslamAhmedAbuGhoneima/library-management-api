from django.contrib import admin
from .models import *
# Register your models here.


class AutherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id', 'name']
    list_filter = ['name']


admin.site.register(Auther, AutherAdmin)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'auther', 'title', 'pages', 'price']
    search_fields = ['id', 'auther', 'description']
    list_filter = ['auther', 'title']
    raw_id_fields = ['auther']


# admin.site.register(Book, BookAdmin)


# class MemberAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user.username']
#     search_fields = ['id', 'user']
#     list_filter = ['id', 'user']


# admin.site.register(Member)

class BorrowAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book']
    list_filter = ['user', 'book']
    search_fields = ['book']


admin.site.register(Borrow, BorrowAdmin)
