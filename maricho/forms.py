from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment, Product, Job, Profile, Blog, Message
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class ProfileForm(forms.ModelForm):
    phone_number = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(initial='ZWE')
    )
    class Meta:
        model = Profile
        fields = ["bio", "profileimg", "coverimg", "location", "phone_number"]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'contact']
        widgets = {
            "caption": forms.Textarea(attrs={"placeholder": "What are you selling today"}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {'body': forms.Textarea(attrs={'placeholder': 'add comment', 'rows': 3})
                   }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_img', 'product_name', 'price', 'category', 'description', 'contact']
        widgets = {'product_name': forms.Textarea(attrs={'placeholder': 'add product', 'rows': 3}),
                   'description': forms.Textarea(attrs={'placeholder': 'product description', 'rows': 3})}

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['company_name', 'position', 'description', 'job_category']
        widgets = {"description": forms.Textarea(attrs={"placeholder": "Write your message", 'class': 'form-control', 'rows': 3})}

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'image', 'body']
        widgets = {'title': forms.Textarea(attrs={'placeholder': 'add title', 'rows': 3}),
                   'body': forms.Textarea(attrs={'placeholder': 'write your story here', 'rows': 3})}