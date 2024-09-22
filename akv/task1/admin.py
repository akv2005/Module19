from django.contrib import admin
from .models import *
# Register your models here.

#admin.site.register(Buyer)
@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance', 'age')


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'cost', 'age_limited')
    search_fields = ('title', 'cost')
    list_filter = ('buyer', 'title', 'cost', 'age_limited', 'size')