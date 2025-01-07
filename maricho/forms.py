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

from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "description",
            "industry",
            "location",
            "employment_type",
            "job_location",
            "salary",
            "skills",
            "qualifications",
            "application_deadline",

        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter job title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Describe the job"}),
            "industry": forms.Select(attrs={"class": "form-control"}),
            "location": forms.Select(attrs={"class": "form-control"}),
            "employment_type": forms.Select(attrs={"class": "form-control"}),
            "job_location": forms.Select(attrs={"class": "form-control"}),
            "salary": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter salary"}),
            "skills": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Enter skills required"}),
            "qualifications": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Enter qualifications"}),
            "application_deadline": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'image', 'body']
        widgets = {'title': forms.Textarea(attrs={'placeholder': 'add title', 'rows': 3}),
                   'body': forms.Textarea(attrs={'placeholder': 'write your story here', 'rows': 3})}

from django import forms
from .models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            "first_name",
            "last_name",
            "email",
            "status",
            "score",
            "assigned_to",
            "phone",
            "last_contacted",
            "next_follow_up",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "score": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Score"}),
            "assigned_to": forms.Select(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
            "last_contacted": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "next_follow_up": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
        }

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "assigned_to",
            "due_date",
            "completed",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Task Title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Task Description"}),
            "assigned_to": forms.Select(attrs={"class": "form-control"}),
            "due_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "name",
            "email",
            "phone",
            "address",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Customer Name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Address"}),
        }
from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            "customer",
            "total",
        ]
        widgets = {
            "customer": forms.Select(attrs={"class": "form-control"}),
            "total": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Total Amount"}),
        }

from django import forms
from .models import InvoiceItem

class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ["invoice", "product", "quantity", "price"]
        widgets = {
            "invoice": forms.Select(attrs={"class": "form-control"}),
            "product": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
        }
from django import forms
from .models import NewsCategory

class NewsCategoryForm(forms.ModelForm):
    class Meta:
        model = NewsCategory
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Category Name"}),
        }
from django import forms
from .models import NewsPost

class NewsPostForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = ["title", "content", "category", "image", "published"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Post Title"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Write your post content..."}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "published": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
        }
from django import forms
from .models import NewsComment

class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComment
        fields = ["post", "author", "content"]
        widgets = {
            "post": forms.Select(attrs={"class": "form-control"}),
            "author": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Write your comment..."}),
        }

from django import forms
from .models import NewsComment

class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComment
        fields = ["post", "author", "content"]
        widgets = {
            "post": forms.Select(attrs={"class": "form-control"}),
            "author": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Write your comment..."}),
        }

from django import forms
from .models import Advertisement

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ["name", "description", "image", "targeted_location", "targeted_keywords", "start_date", "end_date", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ad Name"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Ad Description"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "targeted_location": forms.TextInput(attrs={"class": "form-control", "placeholder": "Location"}),
            "targeted_keywords": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Keywords (comma-separated)"}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["location", "property_type", "title", "rooms", "bedrooms", "bathrooms", "description", "size", "price"]
        widgets = {
            "location": forms.Select(attrs={"class": "form-control"}),
            "property_type": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Property Title"}),
            "rooms": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "bedrooms": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "bathrooms": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Property Description"}),
            "size": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Size (in square meters)"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Price in USD"}),
        }

from django import forms
from .models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["listing", "image"]
        widgets = {
            "listing": forms.Select(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }
from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["listing", "user", "stars", "comment"]
        widgets = {
            "listing": forms.Select(attrs={"class": "form-control"}),
            "user": forms.Select(attrs={"class": "form-control"}),
            "stars": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 5}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Write your review here..."}),
        }

from django import forms
from .models import Page

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ["user", "title", "slug", "content", "is_published"]
        widgets = {
            "user": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Page Title"}),
            "slug": forms.TextInput(attrs={"class": "form-control", "placeholder": "Unique Slug"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 6, "placeholder": "Enter JSON content"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file']


from django import forms
from .models import JobSeeker

class JobSeekerForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = [
            "user", "bio", "phone_number", "image", "industry",
            "country", "resume", "skills", "education", "coverimg"
        ]
        widgets = {
            "user": forms.Select(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Brief biography"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone number"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "industry": forms.Select(attrs={"class": "form-control"}),
            "country": forms.Select(attrs={"class": "form-control"}),
            "resume": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "skills": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Skills"}),
            "education": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Education background"}),
            "coverimg": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }

from django import forms
from .models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            "user", "company_id", "name", "industry", "description",
            "phone_number", "email", "logo", "location", "website"
        ]
        widgets = {
            "user": forms.Select(attrs={"class": "form-control"}),
            "company_id": forms.NumberInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Company name"}),
            "industry": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Description"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone number"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email address"}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "location": forms.Select(attrs={"class": "form-control"}),
            "website": forms.URLInput(attrs={"class": "form-control", "placeholder": "Website URL"}),
        }

from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            "user", "company_id", "name", "industry", "description",
            "phone_number", "email", "logo", "location", "website"
        ]
        widgets = {
            "user": forms.Select(attrs={"class": "form-control"}),
            "company_id": forms.NumberInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Property name"}),
            "industry": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Description"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone number"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email address"}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "location": forms.Select(attrs={"class": "form-control"}),
            "website": forms.URLInput(attrs={"class": "form-control", "placeholder": "Website URL"}),
        }





