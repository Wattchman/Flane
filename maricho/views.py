from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.db import models
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from django.db.models import Sum
from .models import Profile, Post, Comment, LikePost, Follow, \
    Product, Category, Job, Job_category, Blog, Message, Lead, Task, Customer, \
    Invoice, InvoiceItem, NewsComment, NewsPost, NewsCategory, \
    Advertisement, UserActivity, AdImpression, \
    Company, JobSeeker, Image, Listing, Property, Rating, Video, Vid_Like, Vid_Comment
from django.contrib import messages
from django.template.loader import render_to_string
import weasyprint
import decimal
from django.core.exceptions import ValidationError
from Flane import settings
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm, ProductForm, JobForm, ProfileForm, \
    BlogForm, LeadForm, TaskForm, InvoiceForm, InvoiceItemForm, \
    CustomerForm, NewsCommentForm, CompanyForm, \
    JobSeekerForm, ListingForm, PropertyForm, VideoForm
from django.db.models import Q
import redis
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from channels.layers import channel_layers
import random

def generate_unique_id():
    return str(uuid.uuid4())
@login_required(login_url='signin')
@csrf_exempt
@api_view(['POST'])
def send_message(request):
    sender = request.user
    receiver = User.objects.get(username=request.data['receiver'])
    body = request.data['body']
    message = Message.objects.create(sender=sender, receiver=receiver, body=body)
    message_data = {'id': message.id, 'sender': sender.username,
                    'body': body,
                    'timestamp': message.timestamp.strftime('%Y-%m-%d%H:%M:%S')}
    group_name ='user_{}'.format(receiver.id)
    channel_layers.group_send(group_name, {'type': 'new_message', 'message': message_data})

    return Response(message_data)
# r = redis.Redis(host=settings.REDIS_HOST,
    #           port=settings.REDIS_PORT,
#        db=settings.REDIS_DB)


# Create your views here.
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['lastname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname, last_name=lastname)
                user.save()

                # log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)


                return redirect('choice')
        else:
            messages.info(request, 'Passwords not matching')
            return redirect('signup')
    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Credentials are Invalid')
            return redirect('signin')


    else:
        return render(request, 'login.html')


@login_required(login_url='signin')
def product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()

            return redirect('home')
    else:
        form = ProductForm()
        messages.info(request, 'Method is Not Post')

    return render(request, 'product.html', {'form': form})


@login_required(login_url='signin')
def product_detail(request, product_id, product_name):
    product = Product.objects.get(id=product_id)
    profiles = Profile.objects.all()

    for profile in profiles:
        if profile.user == product.user:
            return render(request, 'product_detail.html', {'product': product, 'profile': profile})

    return render(request, 'product_detail.html', {'product': product, 'profile': profile})



def categories(request):
    search_category = request.GET.get('query')
    category_s = Category.objects.filter(name=search_category)
    return render(request, 'category.html', {'category_s': category_s})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, created_at__year=year
                             , created_at__month=month,
                             created_at__day=day)
    return render(request, 'detail.html', {'post': post})



def home(request):
    if hasattr(request, 'user_id'):
        user = request.user

    else:
        user = AnonymousUser()


    blogs = Blog.objects.all()
    categories = Category.objects.all()
    current_user_p = Profile.objects.all()
    videos = list(Video.objects.all())
    random.shuffle(videos)
    j_categories = Job_category.objects.all()
    products = list(Product.objects.all())
    random.shuffle(products)



    random_list= list(Post.objects.all())

    random.shuffle(random_list)

    for post in random_list:
        post.slug = post.caption

        slug = post.slug

    profiles = Profile.objects.all()
    jobs = Job.objects.all()
    followers = Follow.objects.all()
    likes = LikePost.objects.all()
    comment_forms = CommentForm()
    if user == AnonymousUser():
        pass
    else:
        recent_activities = UserActivity.objects.filter(user=user).order_by('-activity_time')[:10]
        keywords = {activity.additional_data.get('keyword') for activity in recent_activities if activity.additional_data}

    ads = Advertisement.objects.all()[:len(random_list)]
    ads = list(ads)
    random.shuffle(ads)
    post_ad_pairs = []
    for i, post in enumerate(random_list):
        post_ad_pairs.append({
            'post': post,
            'ad': ads[i] if i < len(ads) else None
        })


    for ad in ads:
        # Track ad impression
        if user == AnonymousUser():
            pass
        else:
            AdImpression.objects.create(user=user, advertisement=ad, impression_time=timezone.now())

    context = {'post_ad_pairs': post_ad_pairs, 'profiles': profiles, 'c_u_ps': current_user_p,
               'products': products, 'j_categories': j_categories,
               'categories': categories, 'comment_forms': comment_forms,
               'jobs': jobs, 'followers': followers, 'likes': likes, 'blogs': blogs, 'videos': videos}

    return render(request, 'homedj.html', context)


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def choice(request):
    return render(request, 'choice.html')

@login_required(login_url='signin')
def settings(request):

    if request.method == 'POST':

        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.id_user = request.user.id
            user_profile.save()

            return redirect('home')

    else:
        form = ProfileForm()

    return render(request, 'settings.html', {'form': form})

@login_required(login_url='signin')
def company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company_prof = form.save(commit=False)
            company_prof.user = request.user
            company_prof.save()

            return redirect('company_profile', company_prof.id)

    else:
        form = CompanyForm()

    return render(request, 'job/company_registration.html', {'form': form})

def property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_prof = form.save(commit=False)
            property_prof.user = request.user
            property_prof.save()

            return redirect('property_profile', property_prof.id)

    else:
        form = PropertyForm()

    return render(request, 'prop/registration.html', {'form': form})


@login_required(login_url='signin')
def job_seeker(request):
    if request.method == 'POST':
        form = JobSeekerForm(request.POST, request.FILES)
        if form.is_valid():
            job_prof = form.save(commit=False)
            job_prof.user = request.user
            job_prof.save()

            return redirect('jobseeker_profile', job_prof.id)
    else:
        form = JobSeekerForm()

    return render(request, 'job/jobseeker_registration.html', {'form': form})



@login_required(login_url='signin')
def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    posts = Post.objects.all()
    products = Product.objects.all()

    return render(request, 'profil.html', {'profile': profile, 'posts': posts, 'products': products})

@login_required(login_url='signin')
def profile_update(request, id):
    profile = Profile.objects.get(id=id)

    if request.method =='POST':
        bio = request.POST['bio']
        location = request.POST['location']
        phone_number = request.POST['number']
        profile_img = request.POST['profimg']
        cover_img = request.POST['coverimg']

        profile.user = request.user
        profile.bio = bio
        profile.location = location
        profile.phone_number = phone_number
        profile.profileimg = profile_img
        profile.coverimg = cover_img
        profile.save()
        return redirect('profile')

    else:
        return render(request, 'profile_update.html')


@login_required(login_url='signin')
def post_create(request):
    # If the request is a POST request

    if request.method == "POST":
        # Get the form data from the request

        images = request.FILES.get("images")

        form = PostForm(request.POST, request.FILES)
        # If the form is valid
        if form.is_valid():
            # Save the post object without committing to the database
            post = form.save(commit=False)
            # Set the user of the post to the current user
            post.user = request.user
            post.slug = post.caption

            post.image = images
            # Save the post object to the database
            post.save()



            # Redirect to the post list view
            return redirect("home")
    # If the request is not a POST request, redirect to the post list view
    else:
        form = PostForm()
        messages.info(request, 'Method not Post')

    return render(request, "post_create.html", {'form': form})


def comment_details(request, post_id, slug):
    post = Post.objects.get(id=post_id)
    # total_views = r.incr(f'image:{post.id}:views')
    slug = slug
    profiles = Profile.objects.all()

    return render(request, 'commentdetails.html', {'post': post, 'profiles': profiles,  'total_views': total_views})


def blog_details(request, blog_id, blog_title):
    blog = Blog.objects.get(id=blog_id)
    profiles = Profile.objects.all()

    #total_views = r.incr(f'blog_image:{blog.id}:views')

    return render(request, 'blog-details.html', {'blog': blog, 'profiles': profiles})


@login_required(login_url='signin')
def comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        return JsonResponse({
            'user': comment.user.username,
            'body': comment.body,
            'created': comment.created.strftime('%Y-%m-%d %H:%M'),
            'rating': comment.rating,
            'post_id': post.id
        })
    return JsonResponse({'error': form.errors}, status=400)


def load_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(active=True).order_by('-created')
    return JsonResponse({
        'comments': [
            {
                'user': comment.user.username,
                'body': comment.body,
                'created': comment.created.strftime('%Y-%m-%d %H:%M'),
                'rating': comment.rating
            } for comment in comments
        ],
        'post_id': post.id
        })

def load_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(active=True).order_by('-created')
    return JsonResponse({
        'comments': [
            {
                'user': comment.user.username,
                'body': comment.body,
                'created': comment.created.strftime('%Y-%m-%d %H:%M'),
                'rating': comment.rating
            } for comment in comments
        ],
        'post_id': post.id
    })

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        posts = Post.objects.all()

        like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

        if like_filter == None:

            new_like = LikePost.objects.create(post_id=post_id, username=username)
            new_like.save()
            post.no_of_likes += 1
            post.liked = True
            post.save()
            return JsonResponse({'likes': post.no_of_likes, 'liked': post.liked})

        else:
            like_filter.delete()
            post.no_of_likes -= 1
            post.liked = False
            post.save()
            return JsonResponse({'likes': post.no_of_likes, 'liked': post.liked})



@login_required(login_url='signin')
def follow_profile(request):
    username = request.user.username
    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        profile = Profile.objects.get(id=profile_id)


        follow_filter = Follow.objects.filter(profile_id=profile_id, username=username, followed=profile.user.username).first()

        if follow_filter == None:
            new_follow = Follow.objects.create(profile_id=profile_id, username=username, followed=profile.user.username)
            new_follow.save()
            profile.followers += 1
            profile.followed = True
            profile.save()
            return JsonResponse({'followers': profile.followers, 'followed': profile.followed})


        else:
            follow_filter.delete()
            profile.followers -= 1
            profile.followed = False
            profile.save()
            return JsonResponse({'followers': profile.followers, 'followed': profile.followed})


@login_required(login_url='signin')
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('home')
    else:
        form = BlogForm()
    return render(request, 'blog_create.html', {'form': form})


@login_required(login_url='signin')
def chat(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    messages = Message.objects.all()
    user = request.user

    if request.method == 'POST':
        Message.objects.create(sender=request.user, recipient=profile.user,
                               body=request.POST['body'])

        return redirect('chat', profile_id)

    return render(request, 'chat.html', {'messages': messages, 'profile': profile, 'user': user})


@login_required(login_url='signin')
def job_post(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.company = request.user.company_profile
            job.company_id = request.user.company_profile.id
            job.save()
            return redirect('job-list')
    else:
        form = JobForm()
    return render(request, 'job.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from .models import Company, Job

def company_profile(request, company_id):
    # Fetch the company by ID
    company = get_object_or_404(Company, id=company_id)
    # Fetch all jobs related to this company
    jobs = Job.objects.filter(company=company)

    # Pass the company and its jobs to the template
    context = {
        'company': company,
        'jobs': jobs,
    }
    return render(request, 'job/comp_prof.html', context)

def jobseeker_profile(request, profile_id):
    profile = get_object_or_404(JobSeeker, id=profile_id)

    return render(request, 'job/jobseeker_profile.html', {'profile': profile})

def property_profile(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    # Fetch all jobs related to this company
    listings = Listing.objects.filter(user=property.user)
    # Pass the company and its jobs to the template
    context = {
        'property': property,
        'listings': listings,
    }
    return render(request, 'prop/property_profile.html', context)


def job_list(request):
    # Get all industries for the industry filter dropdown

    # Get all companies with a logo for the logo slider (assuming only companies with logos are displayed)
    companies = Company.objects.filter(logo__isnull=False)
    industries = Job_category.objects.all()

    # Set up the initial job queryset
    jobs = Job.objects.active()

    # Get search parameters
    query = request.GET.get('query', '')


    # Filter jobs based on search input
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query)
        )

    # Filter jobs by industry, if selected


    # Pass the data to the template
    context = {
        'jobs': jobs,
        'companies': companies,
        'industries': industries
    }
    return render(request, 'job/job_portal.html', context)


def job_cat(request):
    query = request.GET.get('query', '')
    categories = Job_category.objects.all()
    jobs = Job.objects.all()

    if query:
        jobs = jobs.filter(job_category_id=query)

    return render(request, 'job-list.html', {'jobs': jobs, 'categories': categories})

def job_details(request, job_id):
    job = Job.objects.get(id=job_id)
    return render(request, 'job/job-details.html', {'job': job})

def job_land(request):

    return render(request, 'job/job_land.html')

def company_list(request):
    companies = Company.objects.all()

    return render(request, 'job/company_list.html', {'companies': companies})

def ajax(request):
    return render(request, 'ajax.html')

@login_required(login_url='signin')
def lead_list(request):
    leads = Lead.objects.all()
    for lead in leads:
        if lead.is_ready_for_follow_up():
            print(f"lead {lead.first_name, lead.last_name} is ready for follow-up!")
    return render(request, 'lead_list.html', {'leads': leads})

@login_required(login_url='signin')
def lead_create(request):
    form = LeadForm()
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lead_list')

    return render(request, 'lead_form.html', {'form': form})

@login_required(login_url='signin')
def lead_update(request, pk):
    lead = Lead.objects.get(pk=pk)
    form = LeadForm(instance=lead)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('lead_list')
    return render(request, 'lead_form.html', {'form': form})

@login_required(login_url='signin')
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required(login_url='signin')
def task_create(request):
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')

    return render(request, 'task_form.html', {'form': form})

@login_required(login_url='signin')
def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            return redirect('add_items', invoice_id=invoice.id)
        form.save()
    else:
        form = InvoiceForm()
        return render(request, 'create_invoice.html', {'form': form})

@login_required(login_url='signin')
def add_items(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if request.method == "POST":
        form = InvoiceItemForm(request.POST)
        if form.is_valid():
            invoice_item = form.save(commit=False)
            invoice_item.invoice = invoice
            invoice_item.save()
            invoice.total = 3.02
            invoice.save()
            return redirect('invoice_detail', invoice_id=invoice.id)
    else:
        form = InvoiceForm()
    return render(request, 'add_items.html', {'form': form, 'invoice': invoice})

@login_required(login_url='signin')
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    items = invoice.items.all()

    html_string = render_to_string('invoice_pdf.html', {'invoice': invoice, 'items': items })
    html = weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf(stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=invoice_{invoice.id}.pdf'
    return response

@login_required(login_url='signin')
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'create_customer.html', {'form': form})

@login_required(login_url='signin')
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', customer_id=customer.id)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'edit_customer.html', {'form': form})

@login_required(login_url='signin')
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})

def n_post_list(request):
    posts = NewsPost.objects.all().prefetch_related('comments')
    categories = NewsCategory.objects.all()
    form = NewsCommentForm()

    if request.method == 'POST':
        form = NewsCommentForm(request.POST)
        if form.is_valid():
            for post in posts:
                comment = form.save(commit=False)
                comment.post = post
                comment.save()


        return redirect('n_post_list')
    latest_news = NewsPost.latest_news()
    return render(request,
                  'news/list.html',
                  {'posts': posts, 'categories': categories, 'form': form, 'latest_news': latest_news})

def n_post_detail(request, pk, news_title):
    post = get_object_or_404(NewsPost, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        comments = NewsComment.objects.filter(post=post)
        form = NewsCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()


            return redirect('n_post_detail', pk, news_title)
    else:
        form = NewsCommentForm()

    return render(request, 'news/n_post_detail.html', {
                'post': post,
                'comments': comments,
                'form': form
            })

def n_post_detail_c(request, category_name, pk, news_title):
    post = get_object_or_404(NewsPost, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        comments = NewsComment.objects.filter(post=post)
        form = NewsCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()


            return redirect('n_post_detail_c', category_name, pk, news_title)
    else:
        form = NewsCommentForm()
    categories = NewsCategory.objects.all()
    for category in categories:
        if category.name == category_name:
            posts = NewsPost.objects.filter(category=category)
    return render(request, 'news/n_post_detail.html', {
                'post': post,
                'comments': comments,
                'form': form
            })

def news_category(request, category_name):
    categories = NewsCategory.objects.all()
    for category in categories:
        if category.name == category_name:
            posts = NewsPost.objects.filter(category=category)
    latest_news = NewsPost.latest_news()
    return render(request, 'news/list.html', {'posts': posts, 'categories': categories, 'latest_news': latest_news})


def maricho_business(request):

    return render(request, 'business/maricho_business.html')

def graphic_design(request):

    return render(request, 'business/graphic_design.html')

def ai(request):

    return render(request, 'business/ai.html')

def finance(request):

    return render(request, 'business/finance.html')

def company_reg(request):

    return render(request, 'business/companyreg.html')

def web_dev(request):

    return render(request, 'business/webdev.html')

@login_required
def get_relevant_ads(request):
    user = request.user
    recent_activities = UserActivity.objects.filter(user=user).order_by('-activity_time')[:10]
    keywords = {activity.additional_data.get('keyword') for activity in recent_activities if activity.additional_data}

    ads = Advertisement.objects.all()

    for ad in ads:
        # Track ad impression
        AdImpression.objects.create(user=user, advertisement=ad, impression_time=timezone.now())

    return render(request, 'homedj.html', {'ads': ads})

# views.py (continued)

@login_required
def dashboard(request):
    ads = Advertisement.objects.all()
    user_activities = UserActivity.objects.all().order_by('-activity_time')
    ad_impressions = AdImpression.objects.all()

    # Calculate CTR (Click-through rate) for each ad
    ad_stats = []
    ad_names = []
    impressions_list = []
    clicks_list = []
    ctr_list = []

    for ad in ads:
        impressions = ad.adimpression_set.count()
        clicks = ad.adimpression_set.aggregate(models.Sum('clicks'))['clicks__sum'] or 0
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        ad_stats.append({'ad': ad, 'impressions': impressions, 'clicks': clicks, 'ctr': ctr})

        ad_names.append(ad.name)
        impressions_list.append(impressions)
        clicks_list.append(clicks)
        ctr_list.append(ctr)
        ad_stats.append({'ad': ad, 'impressions': impressions, 'clicks': clicks, 'ctr': ctr})

    context = {
        'ad_stats': ad_stats,
        'user_activities': user_activities,
        'ad_names': ad_names, 'impressions_list': impressions_list,
        'clicks_list': clicks_list, 'ctr_list': ctr_list}
    return render(request, 'ads/dashboard.html', context)


@login_required
def track_ad_click(request, ad_id):
    ad_impression = AdImpression.objects.filter(user=request.user, advertisement_id=ad_id).first()
    if ad_impression:
        ad_impression.clicks += 1
        ad_impression.save()
    return JsonResponse({'status': 'success'})


  # chat functions
def chat(request, recipient_id):
    # Retrieve messages between the user and another user
    try:
        recipient = User.objects.get(id=recipient_id)
    except User.DoesNotExist:
        raise Http404("User does not exist")


    return render(request,
                  'messaging/chat.html',
                  {'recipient': recipient, 'user_id': request.user.id, 'recipient_id': recipient.id})



def create_listing(request):
    if request.method == 'POST':
        listing_form = ListingForm(request.POST, request.FILES)

        if listing_form.is_valid():

            listing = listing_form.save(commit=False)
            listing.user = request.user
            listing.save()
            images = request.FILES.getlist('images')
            for image_file in images:
                Image.objects.create(listing=listing, image=image_file)
            return redirect('property-list')  # Replace with your success URL

    else:
        listing_form = ListingForm()


    context = {
        'listing_form': listing_form,
    }
    return render(request, 'prop/create_listing.html', context)

def property_list(request):
    properties = Listing.objects.prefetch_related('images').all()
    city = request.GET.get('city', '')
    listing_type = request.GET.get('listing_type', '')

    cities = Listing.objects.values_list('location', flat=True).distinct()
    if city:
        properties = properties.filter(location__icontains=city)
    if listing_type:
        properties = properties.filter(property_type__iexact=listing_type)


    return render(request, 'prop/listings.html', {'properties': properties,
                                                  'cities': cities,
                                                  'city': city,
                                                  'listing_type': listing_type})

def listing_detail(request, listing_id):
    listing = Listing.objects.prefetch_related('images').get(id=listing_id)
    profile = Property.objects.get(user=listing.user)

    return render(request, 'prop/listing_detail.html', {'listing': listing, 'profile': profile})

def listing_ratings(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    ratings = listing.ratings.all().values('stars', 'comment', 'created_at')
    return JsonResponse({'ratings': list(ratings)})



@login_required
def add_rating(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    stars = int(request.POST.get('stars'))
    comment = request.POST.get('comment')

    # Save rating
    rating = Rating.objects.create(listing=listing, user=request.user, stars=stars, comment=comment)
    return JsonResponse({'stars': rating.stars, 'comment': rating.comment, 'username': rating.user.username})
from django.shortcuts import render, get_object_or_404
from .models import Page

def page_editor(request, slug):
    page = get_object_or_404(Page, slug=slug, user=request.user)
    return render(request, 'pages/editor.html', {'page': page})

from django.shortcuts import render, get_object_or_404

def render_page(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, 'render_page.html', {'content': page.content})

def save_page(request):
    if request.method == "POST":
        data = json.loads(request.body)
        slug = data.get('slug')
        content = data.get('content')

        # Save the content to the database
        page = get_object_or_404(Page, slug=slug, user=request.user)
        page.content = content
        page.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PageForm

@login_required
def create_page(request):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.user = request.user  # Associate the page with the logged-in user
            page.save()
            return redirect('page_editor', slug=page.slug)  # Redirect to the editor
    else:
        form = PageForm()
    return render(request, 'pages/create_page.html', {'form': form})
def video_upload(request):
    """Handle video file uploads with a size limit of 20 MB."""
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Save the video if it passes validation
                video = form.save(commit=False)
                video.user = request.user
                video.user_id = request.user.id
                video.save()
                messages.success(request, "Video uploaded successfully!")
                return redirect('home')
            except ValidationError as e:
                messages.error(request, e.message)
        else:
            messages.error(request, "Invalid form submission. Please check your input.")
    else:
        form = VideoForm()
    return render(request, 'videos/video_upload.html', {'form': form})

@login_required
@csrf_exempt
def toggle_like(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    like, created = Vid_Like.objects.get_or_create(video=video, user=request.user)
    if not created:
        like.delete()
        return JsonResponse({"liked": False, "like_count": video.likes.count()})
    return JsonResponse({"liked": True, "like_count": video.likes.count()})

@login_required
@csrf_exempt
def add_comment(request, video_id):
    if request.method == "POST":
        video = get_object_or_404(Video, id=video_id)
        content = request.POST.get("content")
        comment = Vid_Comment.objects.create(video=video, user=request.user, content=content)
        return JsonResponse({
            "user": comment.user.username,
            "content": comment.content,
            "created_at": comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

@login_required
def fetch_comments(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    comments = video.comments.order_by("-created_at").values("user__username", "content", "created_at")
    return JsonResponse(list(comments), safe=False)

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return JsonResponse({
        "id": video.id,
        "title": video.title,
        "description": video.description,
        "video_url": video.video_file.url,
        "like_count": video.likes.count(),
        "liked": video.likes.filter(user=request.user).exists() if request.user.is_authenticated else False,
    })
