from django.urls import path
from .import views
urlpatterns = [
    path('ajax', views.ajax, name='ajax'),
    path('blog-details/<int:blog_id>/<str:blog_title>', views.blog_details, name='blog-details'),
    path('blog_create', views.blog_create, name='blog_create'),
    path('job-details/<int:job_id>', views.job_details, name='job-details'),
    path('job-list/', views.job_list, name='job-list'),
    path('job-cat/', views.job_cat, name='job-cat'),
    path('chat/<int:profile_id>', views.chat , name='chat'),
    path('<int:year>/<int:month>/<int:day>/<slug:post/', views.post_detail, name='post_detail'),
    path('signup', views.signup, name='signup'),
    path('job', views.job_post, name='job'),
    path('like-post', views.like_post, name='like-post'),
    path('follow-profile', views.follow_profile, name='follow-profile'),
    path('signin', views.signin, name='signin'),
    path('product', views.product_view, name='product'),
    path('product-details/<int:product_id>/<str:product_name>', views.product_detail, name='product-details'),
    path('home', views.home, name='home'),
    path('logout', views.logout, name='logout'),
    path('chat', views.send_message, name='chat'),
    path('settings', views.settings, name='settings'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('profile-update/<int:id>', views.profile_update, name='profile-update'),
    path('post', views.post_create, name='post'),
    path('comment/<int:post_id>', views.comment_view, name='comment'),
    path('category/', views.categories, name='category'),
    path('comment-details/<int:post_id>/<slug:slug>', views.comment_details, name='comment_details')
]