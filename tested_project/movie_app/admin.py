from django.contrib import admin
from . models import Category,Movie,Review

# Register your models here.
class categoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug',]
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Category,categoryAdmin)
class productAdmin(admin.ModelAdmin):
    list_display = ['name','date']
    list_editable = ['date']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20
admin.site.register(Movie,productAdmin)
admin.site.register(Review)