from django.db import models
import decimal
from django.db.models import Max
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import random
from django.core.exceptions import ValidationError

COUNTRY_CHOICES = [
    ("Afghanistan", "Afghanistan"), ("Albania", "Albania"), ("Algeria", "Algeria"),
    ("Andorra", "Andorra"), ("Angola", "Angola"), ("Antigua and Barbuda", "Antigua and Barbuda"),
    ("Argentina", "Argentina"), ("Armenia", "Armenia"), ("Australia", "Australia"),
    ("Austria", "Austria"), ("Azerbaijan", "Azerbaijan"), ("Bahamas", "Bahamas"),
    ("Bahrain", "Bahrain"), ("Bangladesh", "Bangladesh"), ("Barbados", "Barbados"),
    ("Belarus", "Belarus"), ("Belgium", "Belgium"), ("Belize", "Belize"),
    ("Benin", "Benin"), ("Bhutan", "Bhutan"), ("Bolivia", "Bolivia"),
    ("Bosnia and Herzegovina", "Bosnia and Herzegovina"), ("Botswana", "Botswana"),
    ("Brazil", "Brazil"), ("Brunei", "Brunei"), ("Bulgaria", "Bulgaria"),
    ("Burkina Faso", "Burkina Faso"), ("Burundi", "Burundi"), ("Cabo Verde", "Cabo Verde"),
    ("Cambodia", "Cambodia"), ("Cameroon", "Cameroon"), ("Canada", "Canada"),
    ("Central African Republic", "Central African Republic"), ("Chad", "Chad"), ("Chile", "Chile"),
    ("China", "China"), ("Colombia", "Colombia"), ("Comoros", "Comoros"),
    ("Congo, Democratic Republic of the", "Congo, Democratic Republic of the"),
    ("Congo, Republic of the", "Congo, Republic of the"), ("Costa Rica", "Costa Rica"),
    ("Côte d'Ivoire", "Côte d'Ivoire"), ("Croatia", "Croatia"), ("Cuba", "Cuba"),
    ("Cyprus", "Cyprus"), ("Czech Republic", "Czech Republic"), ("Denmark", "Denmark"),
    ("Djibouti", "Djibouti"), ("Dominica", "Dominica"), ("Dominican Republic", "Dominican Republic"),
    ("Ecuador", "Ecuador"), ("Egypt", "Egypt"), ("El Salvador", "El Salvador"),
    ("Equatorial Guinea", "Equatorial Guinea"), ("Eritrea", "Eritrea"), ("Estonia", "Estonia"),
    ("Eswatini", "Eswatini"), ("Ethiopia", "Ethiopia"), ("Fiji", "Fiji"),
    ("Finland", "Finland"), ("France", "France"), ("Gabon", "Gabon"),
    ("Gambia", "Gambia"), ("Georgia", "Georgia"), ("Germany", "Germany"),
    ("Ghana", "Ghana"), ("Greece", "Greece"), ("Grenada", "Grenada"),
    ("Guatemala", "Guatemala"), ("Guinea", "Guinea"), ("Guinea-Bissau", "Guinea-Bissau"),
    ("Guyana", "Guyana"), ("Haiti", "Haiti"), ("Honduras", "Honduras"),
    ("Hungary", "Hungary"), ("Iceland", "Iceland"), ("India", "India"),
    ("Indonesia", "Indonesia"), ("Iran", "Iran"), ("Iraq", "Iraq"),
    ("Ireland", "Ireland"), ("Israel", "Israel"), ("Italy", "Italy"),
    ("Jamaica", "Jamaica"), ("Japan", "Japan"), ("Jordan", "Jordan"),
    ("Kazakhstan", "Kazakhstan"), ("Kenya", "Kenya"), ("Kiribati", "Kiribati"),
    ("Korea, North", "Korea, North"), ("Korea, South", "Korea, South"),
    ("Kuwait", "Kuwait"), ("Kyrgyzstan", "Kyrgyzstan"), ("Laos", "Laos"),
    ("Latvia", "Latvia"), ("Lebanon", "Lebanon"), ("Lesotho", "Lesotho"),
    ("Liberia", "Liberia"), ("Libya", "Libya"), ("Liechtenstein", "Liechtenstein"),
    ("Lithuania", "Lithuania"), ("Luxembourg", "Luxembourg"), ("Madagascar", "Madagascar"),
    ("Malawi", "Malawi"), ("Malaysia", "Malaysia"), ("Maldives", "Maldives"),
    ("Mali", "Mali"), ("Malta", "Malta"), ("Marshall Islands", "Marshall Islands"),
    ("Mauritania", "Mauritania"), ("Mauritius", "Mauritius"), ("Mexico", "Mexico"),
    ("Micronesia", "Micronesia"), ("Moldova", "Moldova"), ("Monaco", "Monaco"),
    ("Mongolia", "Mongolia"), ("Montenegro", "Montenegro"), ("Morocco", "Morocco"),
    ("Mozambique", "Mozambique"), ("Myanmar", "Myanmar"), ("Namibia", "Namibia"),
    ("Nauru", "Nauru"), ("Nepal", "Nepal"), ("Netherlands", "Netherlands"),
    ("New Zealand", "New Zealand"), ("Nicaragua", "Nicaragua"), ("Niger", "Niger"),
    ("Nigeria", "Nigeria"), ("North Macedonia", "North Macedonia"), ("Norway", "Norway"),
    ("Oman", "Oman"), ("Pakistan", "Pakistan"), ("Palau", "Palau"),
    ("Palestine", "Palestine"), ("Panama", "Panama"), ("Papua New Guinea", "Papua New Guinea"),
    ("Paraguay", "Paraguay"), ("Peru", "Peru"), ("Philippines", "Philippines"),
    ("Poland", "Poland"), ("Portugal", "Portugal"), ("Qatar", "Qatar"),
    ("Romania", "Romania"), ("Russia", "Russia"), ("Rwanda", "Rwanda"),
    ("Saint Kitts and Nevis", "Saint Kitts and Nevis"), ("Saint Lucia", "Saint Lucia"),
    ("Saint Vincent and the Grenadines", "Saint Vincent and the Grenadines"),
    ("Samoa", "Samoa"), ("San Marino", "San Marino"), ("Sao Tome and Principe", "Sao Tome and Principe"),
    ("Saudi Arabia", "Saudi Arabia"), ("Senegal", "Senegal"), ("Serbia", "Serbia"),
    ("Seychelles", "Seychelles"), ("Sierra Leone", "Sierra Leone"), ("Singapore", "Singapore"),
    ("Slovakia", "Slovakia"), ("Slovenia", "Slovenia"), ("Solomon Islands", "Solomon Islands"),
    ("Somalia", "Somalia"), ("South Africa", "South Africa"), ("Spain", "Spain"),
    ("Sri Lanka", "Sri Lanka"), ("Sudan", "Sudan"), ("Sudan, South", "Sudan, South"),
    ("Suriname", "Suriname"), ("Sweden", "Sweden"), ("Switzerland", "Switzerland"),
    ("Syria", "Syria"), ("Taiwan", "Taiwan"), ("Tajikistan", "Tajikistan"),
    ("Tanzania", "Tanzania"), ("Thailand", "Thailand"), ("Timor-Leste", "Timor-Leste"),
    ("Togo", "Togo"), ("Tonga", "Tonga"), ("Trinidad and Tobago", "Trinidad and Tobago"),
    ("Tunisia", "Tunisia"), ("Turkey", "Turkey"), ("Turkmenistan", "Turkmenistan"),
    ("Tuvalu", "Tuvalu"), ("Uganda", "Uganda"), ("Ukraine", "Ukraine"),
    ("United Arab Emirates", "United Arab Emirates"), ("United Kingdom", "United Kingdom"),
    ("United States", "United States"), ("Uruguay", "Uruguay"), ("Uzbekistan", "Uzbekistan"),
    ("Vanuatu", "Vanuatu"), ("Vatican City", "Vatican City"), ("Venezuela", "Venezuela"),
    ("Vietnam", "Vietnam"), ("Yemen", "Yemen"), ("Zambia", "Zambia"), ("Zimbabwe", "Zimbabwe"),
]

# Create your models here
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} to {self.recipient}: {self.content[:20]}"


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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
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

class Job_category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.name}'

class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='jobseeker')
    bio = models.TextField(blank=True)
    phone_number = PhoneNumberField(blank=True)
    image = models.ImageField(upload_to='job_profile_images/')
    industry = models.ForeignKey(Job_category, on_delete=models.CASCADE, related_name='jobseekers')
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    coverimg = models.ImageField(upload_to='job_cover_images/', default=False)

    def __str__(self):
        return self.user.username

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company_profile")
    company_id = models.IntegerField(default=1)
    name = models.CharField(max_length=100, unique=True)
    industry = models.ForeignKey(Job_category, on_delete=models.CASCADE, related_name="companies")
    description = models.TextField(blank=True)
    phone_number = PhoneNumberField(blank=True)
    email = models.EmailField()
    logo = models.ImageField(upload_to='profile_images/')
    location = models.CharField(max_length=100, choices=COUNTRY_CHOICES)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Property(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="property_profile")
    company_id = models.IntegerField(default=1)
    name = models.CharField(max_length=100, unique=True)
    industry = models.ForeignKey(Job_category, on_delete=models.CASCADE, related_name="properties")
    description = models.TextField(blank=True)
    phone_number = PhoneNumberField(blank=True)
    email = models.EmailField()
    logo = models.ImageField(upload_to='property_images/')
    location = models.CharField(max_length=100, choices=COUNTRY_CHOICES)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.name}'



class NewsCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product')
    product_img = models.ImageField(upload_to='window_images')
    story_img = models.ImageField(upload_to='story_images', null=True)
    product_name = models.TextField(blank=True)
    description = models.TextField(blank=True)
    price = models.FloatField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True)
    time = models.DateTimeField(auto_now_add=True)
    contact = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return f"{self.product_name}"

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
    caption = models.TextField(max_length=350, blank=True)
    title = models.TextField(blank=True, max_length=30)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=1)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'



class Follow(models.Model):
    username = models.CharField(max_length=100)
    profile_id = models.CharField(max_length=100)
    followed = models.CharField(max_length=100,blank=True)

class JobQuerySet(models.QuerySet):
    def active(self):
        return self.filter(application_deadline__gte=timezone.now())
class Job(models.Model):

    # Choices for employment types and job locations
    EMPLOYMENT_TYPE_CHOICES = [
        ("FT", "Full-time"),
        ("PT", "Part-time"),
        ("CT", "Contract"),
        ("FL", "Freelance"),
        ("IN", "Internship"),
    ]

    JOB_LOCATION_CHOICES = [
        ("ON", "On-site"),
        ("RE", "Remote"),
        ("HY", "Hybrid"),
    ]

    # Core job fields
    title = models.TextField(max_length=100, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    description = models.TextField()
    industry = models.ForeignKey(Job_category, on_delete=models.CASCADE, related_name='jobsi')
    location = models.CharField(max_length=100, choices=COUNTRY_CHOICES, null=True)
    employment_type = models.CharField(
        max_length=2,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default="FT"
    )
    job_location = models.CharField(
        max_length=2,
        choices=JOB_LOCATION_CHOICES,
        default="ON"
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs_posted", null=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    skills = models.TextField(default="skills required")
    qualifications = models.TextField(default="Enter qualifications")
    application_deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    objects = JobQuerySet.as_manager()
    def __str__(self):
        return f"{self.title} at {self.company}"

    class Meta:
        ordering = ["-posted_date"]


class Lead(models.Model):
    STATUS_CHOICES = (('New', 'New'),
                      ('Contacted', 'Contacted'),
                      ('Qualified', 'Qualified'),
                      ('Converted', 'Converted'),
                      ('Unqualified', 'Unqualified'),
                      )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    score = models.IntegerField(default=0)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL,
                                    null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_contacted = models.DateTimeField(null=True, blank=True)
    next_follow_up = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def is_ready_for_follow_up(self):
        if self.next_follow_up:
            return self.next_follow_up <= timezone.now()
        return False

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(Lead, on_delete=models.CASCADE)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Invoice {self.id} for {self.customer.name}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="items",
                                on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.quantity} x {self.product.product_name}'

    def get_total_price(self):
        return self.price*self.quantity


class Page(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='page')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.JSONField(default=dict)  # For storing customizable sections as JSON
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


    # video models


def validate_file_size(value):
    limit = 20 * 1024 * 1024  # 20 MB in bytes
    if value.size > limit:
        raise ValidationError("File too large. Size should not exceed 20 MB.")

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/', validators=[validate_file_size])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Vid_Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.video.title}"

class Vid_Like(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('video', 'user')

    def __str__(self):
        return f"Like by {self.user.username} on {self.video.title}"
    def __str__(self):
        return self.name

class NewsPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_images', blank=True, null=True)
    published = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    @classmethod
    def latest_news(cls):
        # Get posts from the last 24 hours
        time_threshold = timezone.now() - timedelta(days=1)
        return cls.objects.filter(
            published__gte=time_threshold).order_by('-published')
    class Meta:
        ordering =['-published']


class NewsComment(models.Model):
    post = models.ForeignKey(NewsPost, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.author}'

#models for the advertisement engine and tracking user activity

class Advertisement(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField()
    image = models.ImageField(upload_to='ads/')
    targeted_location = models.CharField(max_length=255, null=True, blank=True)
    targeted_keywords = models.TextField()  # Store keywords as comma-separated values
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)  # e.g., 'post_view', 'product_click'
    activity_time = models.DateTimeField(default=timezone.now)
    additional_data = models.JSONField(null=True, blank=True)  # Stores additional details like post ID, etc.

class AdImpression(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    impression_time = models.DateTimeField(default=timezone.now)
    clicks = models.PositiveIntegerField(default=0)

def get_default_user():
    return User.objects.first().id

class Listing(models.Model):
    LOCATION_CHOICES = [
        ('Harare', 'Harare'),
        ('Bulawayo', 'Bulawayo'),
        ('Mutare', 'Mutare'),
        ('Kwekwe', 'Kwekwe'),
        ('Gweru', 'Gweru'),
        ('Kadoma', 'Kadoma'),
        ('Victoria Falls', 'Victoria Falls'),
        ('Masvingo', 'Masvingo'),
        ('Kariba', 'Kariba'),
        ('Karoi', 'Karoi'),
        ('Chinhoyi', 'Chinhoyi'),
        ('Marondera', 'Marondera'),
        ('Chegutu', 'Chegutu'),
        ('Chitungwiza', 'Chitungwiza'),
        ('Norton', 'Norton'),
        # Add more locations as needed
    ]

    PROPERTY_TYPE_CHOICES = [
        ('for_sale', 'For Sale'),
        ('for_rent', 'For Rent'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    title = models.TextField(default='Enter the title')
    rooms = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    description = models.TextField(default="Enter your description")
    size = models.PositiveIntegerField(help_text="square metres")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property_type.capitalize()} in {self.location} - ${self.price}"

class Rating(models.Model):
    listing = models.ForeignKey(Listing, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.PositiveIntegerField()  # Store star rating, 1-5
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing.title} - {self.stars} stars"



class Image(models.Model):
    listing = models.ForeignKey(Listing, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listing_images/')  # Change here

