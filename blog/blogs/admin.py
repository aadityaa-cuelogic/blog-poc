from django.contrib import admin

# Register your models here.
from .models import Post, Category, Comment, Likes, Imagepost

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Likes)
admin.site.register(Imagepost)
