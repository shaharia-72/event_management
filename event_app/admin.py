from django.contrib import admin
from .models import Category, Event, Participation
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug')
    fields = ('category_name', 'slug')  
    readonly_fields = ('slug',) 

admin.site.register(Category, CategoryAdmin)
admin.site.register(Event)
admin.site.register(Participation)

