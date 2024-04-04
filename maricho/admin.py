from django.contrib import admin
from .models import Profile, Post, \
    Comment, LikePost, Product, Category, Job, Job_category, Follow, Blog, Message
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(LikePost)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Job_category)
admin.site.register(Job)
admin.site.register(Follow)
admin.site.register(Blog)
admin.site.register(Message)
