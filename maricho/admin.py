from django.contrib import admin
from .models import Profile, Post, \
    Comment, LikePost, Product, Category, Job, Job_category, Follow,\
    Blog, Message, Lead, Task, Customer, Invoice, \
    InvoiceItem, NewsPost, NewsCategory, NewsComment, \
    Advertisement, UserActivity, AdImpression, Company, JobSeeker, \
    Listing, Image, Property, Rating, Page, Video, PostImage

# Register your models here.
admin.site.register(Profile)
admin.site.register(PostImage)
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
admin.site.register(Lead)
admin.site.register(Task)
admin.site.register(Customer)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(NewsPost)
admin.site.register(NewsCategory)
admin.site.register(NewsComment)
admin.site.register(Advertisement)
admin.site.register(AdImpression)
admin.site.register(UserActivity)
admin.site.register(Company)
admin.site.register(JobSeeker)
admin.site.register(Image)
admin.site.register(Listing)
admin.site.register(Property)
admin.site.register(Rating)
admin.site.register(Video)

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_published', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}





