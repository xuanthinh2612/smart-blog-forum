from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, Profile


class UserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'birth_day', 'bio', 'avatar']

class UserFormForUpdate(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']  # KHÔNG bao gồm 'password'

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
    #         raise forms.ValidationError("Email này đã được sử dụng.")
    #     return email