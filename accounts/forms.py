from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile, Address




class LoginForm(forms.Form):
    email = forms.EmailField(label='email')
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'password1', 'password2']



class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'birth_date', 'mobile', 'id_code', 'phone', 'card_num', 'is_edited']


class AddressForm(forms.ModelForm):
    class Meta:
        model= Address
        fields = ['profile', 'province', 'city', 'postal_code', 'recipient', 'complete_address']




class ResetPassForm(forms.Form):
    email = forms.EmailField(max_length=150, label= 'Email')


class ResetPassConfirmForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, label='New Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')


class ChangePassForm(forms.Form):
    old_pass = forms.CharField(widget=forms.PasswordInput, label = 'Old Password')
    password1 = forms.CharField(widget=forms.PasswordInput, label='New Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')