from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import *


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirmar Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k: "" for k in fields}





class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']



class PostForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 50, 'placeholder': '¿En qué estás pensando?'}),
        required=True
    )
    image = forms.ImageField(label="Imagen", required=False)
    audio = forms.FileField(label="Audio", required=False)
    video = forms.FileField(label="Video", required=False)

    class Meta:
        model = Post
        fields = ['content', 'image', 'audio', 'video']

        
