from django.db import models
from django.db.models import Max
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.urls import reverse
import random
# Create your models here

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', default=1)
    body = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog')
    title = models.TextField(blank=True, max_length=200)
    image = models.ImageField(upload_to='blog_images')
    body = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    id_user = models.IntegerField(default=0)
    phone_number = PhoneNumberField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default="heart.png")
    location = models.CharField(max_length=100, blank=True)
    followers = models.IntegerField(default=0)
    followed = models.BooleanField(default=False)
    coverimg = models.ImageField(upload_to='cover_images', default=False)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return f'{self.name}'

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product')
    product_img = models.ImageField(upload_to='window_images')
    product_name = models.TextField(blank=True)
    description = models.TextField(blank=True)
    price = models.FloatField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True)
    time = models.DateTimeField(auto_now_add=True)
    contact = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return f'{self.user}: {self.price}'

    class Meta:
      ordering = ['-time']

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

class Post(models.Model):
    # The user field is a foreign key to the
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
  # The image field is an image field that stores the URL of the post image
    image = models.ImageField(upload_to='posts/')

    slug = models.SlugField(max_length=250, unique_for_date='created_at', default=False)
  # The caption field is a text field that stores the caption of the post
    caption = models.TextField(blank=True)
    contact = models.CharField(max_length=100, blank=True)
  # The created_at field is a date time field that stores the creation time of the post
    created_at = models.DateTimeField(auto_now_add=True)
  # The updated_at field is a date time field that stores the update time of the post
    updated_at = models.DateTimeField(auto_now=True)
    no_of_likes = models.IntegerField(default=0)
    liked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}: {self.caption}'

    class Meta:
        ordering = ['-created_at']



    def get_absolute_url(self):
        return reverse('post_detail', args=[self.created_at.year,
                                             self.created_at.month,
                                             self.created_at.day,
                                             self.slug])
class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.CharField(max_length=80)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'



class Follow(models.Model):
    username = models.CharField(max_length=100)
    profile_id = models.CharField(max_length=100)
    followed = models.CharField(max_length=100,blank=True)




class Job_category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.name}'

class Job(models.Model):
    author = models.ForeignKey(User, related_name='job', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=250)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    job_category = models.ForeignKey(Job_category, related_name='jobs', on_delete=models.CASCADE, null=True)
    city = models.TextField()


    def __str__(self):
        return f'{self.author}'

