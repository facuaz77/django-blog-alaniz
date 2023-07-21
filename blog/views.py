from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User


# Create your views here.


def home(request):
    return render(request, 'home.html')


def feed(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'social/feed.html', context)


@login_required
def profile(request, username=None):
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        posts = user.posts.all()
    else:
        posts = current_user.posts.all()
        user = current_user
    return render(request, 'social/profile.html', {'user': user, 'posts': posts})




@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('feed')
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'social/edit_profile.html', {'form': form})




@user_passes_test(lambda u: u.is_superuser)
def delete_post_admin(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, 'Post eliminado correctamente.')
    return redirect('feed')




def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            messages.success(
                request, f'¡Bienvenido, {username}! Tu registro fue un éxito.')
            login(request, user)  # Iniciar sesión automáticamente
            return redirect('feed')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'signup.html', context)



def login_view(request):
    if request.method == 'POST':
        # Procesar formulario de inicio de sesión
        # ...
        return redirect('feed')
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'social/post.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Verificar si el usuario actual es el propietario del post
    if post.user == request.user or request.user.is_superuser:
        post.delete()
        messages.success(request, 'Post eliminado correctamente.')
    else:
        messages.error(request, 'No tienes permiso para eliminar este post.')

    return redirect('feed')




@login_required
def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)  # Agregamos request.FILES al formulario
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post actualizado correctamente.')
            return redirect('feed')
    else:
        form = PostForm(instance=post)

    return render(request, 'social/update_post.html', {'form': form})


def follow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Relations(from_user=current_user, to_user=to_user_id)
    rel.save()
    messages.success(request, f'Sigues a {username}')
    return redirect('profile', username=username)


def unfollow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Relations.objects.filter(
        from_user=current_user.id, to_user=to_user_id).get()
    rel.delete()

    messages.success(request, f'Has dejado de seguir a {username}')
    return redirect('profile', username=username)
