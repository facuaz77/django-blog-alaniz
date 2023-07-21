from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [

    path('', views.home, name='home'),
    path('feed/', views.feed, name='feed'),
    path('signup/', views.signup, name='register'),
    path('login/', LoginView.as_view(template_name='signin.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post/', views.post, name='post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('update_post/<int:post_id>/', views.update_post, name='update_post'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/',views.profile, name='profile'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete_post_admin/<int:post_id>/', views.delete_post_admin, name='delete_post_admin'),




    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


