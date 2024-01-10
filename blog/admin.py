from django.contrib import admin
from .models import Posts,BlogComment,Categorys

# Register your models here.

admin.site.register(BlogComment)
admin.site.register(Categorys)

@admin.register(Posts)

class PostAdmin(admin.ModelAdmin):
    class Media:
        js= ('tinyInject.js',)
