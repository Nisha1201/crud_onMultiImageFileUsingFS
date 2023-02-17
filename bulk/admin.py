from django.contrib import admin
from .models import Image
# Register your models here.

class data_id(admin.ModelAdmin):
    list_display=('id','image')

admin.site.register(Image,data_id)