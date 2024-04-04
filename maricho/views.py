from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Profile, Post, Comment, LikePost, Follow, \
    Product, Category, Job, Job_category, Blog, Message
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm, ProductForm, JobForm, ProfileForm, \
    BlogForm
from django.db.models import Q
import redis
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from channels.layers import channel_layers
import random

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
r = redis.Redis(host=settings.REDIS_HOST,
               port=settings.REDIS_PORT,
               db=settings.REDIS_DB)


# Create your views here.
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
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
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)


                return redirect('settings')
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


def product_detail(request, product_id, product_name):
    product = Product.objects.get(id=product_id)
    profiles = Profile.objects.all()

    for profile in profiles:
        if profile.user == product.user:
            return render(request, 'product_detail.html', {'product': product, 'profile': profile})

    return render(request, 'product_detail.html', {'product': product, 'profile': profile})


@login_required(login_url='signin')
def categories(request):
    search_category = request.GET.get('query')
    category_s = Category.objects.filter(name=search_category)
    return render(request, 'category.html', {'category_s': category_s})


@login_required(login_url='signin')
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, created_at__year=year
                             , created_at__month=month,
                             created_at__day=day)
    return render(request, 'detail.html', {'post': post})


@login_required(login_url='signin')
def home(request):
    blogs = Blog.objects.all()
    categories = Category.objects.all()
    j_categories = Job_category.objects.all()
    products = Product.objects.all()
    current_user_p = Profile.objects.get(user=request.user)
    posts = Post.objects.all()
    all_posts = list(posts)
    random_list = random.choice([all_posts])

    for post in random_list:
        post.slug = post.caption

        slug = post.slug

    profiles = Profile.objects.all()
    jobs = Job.objects.all()
    followers = Follow.objects.all()
    likes = LikePost.objects.all()
    form = CommentForm()

    context = {'posts': random_list, 'profiles': profiles, 'c_u_p': current_user_p,
               'products': products, 'j_categories': j_categories,
               'categories': categories,
               'form': form, 'jobs': jobs, 'followers': followers, 'likes': likes, 'blogs': blogs}

    return render(request, 'home.html', context)


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


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
def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    posts = Post.objects.all()
    products = Product.objects.all()

    return render(request, 'profile.html', {'profile': profile, 'posts': posts, 'products': products})

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
    total_views = r.incr(f'image:{post.id}:views')
    slug = slug
    profiles = Profile.objects.all()

    return render(request, 'commentdetails.html', {'post': post, 'profiles': profiles,  'total_views': total_views})

@login_required(login_url='signin')
def blog_details(request, blog_id, blog_title):
    blog = Blog.objects.get(id=blog_id)
    profiles = Profile.objects.all()

    total_views = r.incr(f'blog_image:{blog.id}:views')

    return render(request, 'blog-details.html', {'blog': blog, 'profiles': profiles, 'total_views': total_views})


@login_required(login_url='signin')
def comment_view(request, post_id):
    post = Post.objects.get(id=post_id)
    profiles = Profile.objects.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)

            comment.post = post

            comment.user = request.user.username

            comment.save()
            return redirect('home')
    else:
        form = CommentForm()
    context = {'form': form, 'post': post, 'profiles': profiles}
    return render(request, 'comment.html', context)


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
            job.author = request.user
            job.save()
            return redirect('home')
    else:
        form = JobForm()
    return render(request, 'job.html', {'form': form})

@login_required(login_url='signin')
def job_list(request):
    query = request.GET.get('query', '')
    categories = Job_category.objects.all()
    jobs = Job.objects.all()

    if query:
        jobs = jobs.filter(Q(position__icontains=query) | Q(description__icontains=query))


    return render(request, 'job-list.html', {'jobs': jobs, 'categories': categories})

@login_required(login_url='signin')
def job_cat(request):
    query = request.GET.get('query', '')
    categories = Job_category.objects.all()
    jobs = Job.objects.all()

    if query:
        jobs = jobs.filter(job_category_id=query)

    return render(request, 'job-list.html', {'jobs': jobs, 'categories': categories})
@login_required(login_url='signin')
def job_details(request, job_id):
    job = Job.objects.get(id=job_id)
    return render(request, 'job-details.html', {'job': job})

def ajax(request):
    return render(request, 'ajax.html')
