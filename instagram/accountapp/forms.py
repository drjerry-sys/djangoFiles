from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class SearchForm(forms.Form):
    search_value = forms.CharField(max_length=25, label='',
                       widget=forms.TextInput(attrs=({'class':"form-control mr-sm-2",'type':"search",
                          'id':"search",'style':"height: 25px; margin: auto 0;", 'placeholder':"search"})))

username1 = 'Obaloluwa'
class EditProfile1(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'username', 'email')
        labels = {
            'first_name': 'Name',
            'email': 'Email',
        }
        help_texts = {
            'first_name': 'Help people discover your account by using the name you\'re known by: either your full name, nickname, or business name.\
                                <br><br>You can only change your name twice within 14 days.',
            'username': f'In most cases, you\'ll be able to change your username back to {username1} for another 14 days. <a href="#">Learn More</a>',
        }


class EditProfile2(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'phone', 'gender', 'bio', 'profile_pics')
        label = {
            'profile_pics': '',
        }

class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        help_texts = {
            'username': 'this is required to be unique to the user',
        }
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password2'] != cd['password']:
            raise forms.ValidationError('Password do not match')

class ConfirmReg(forms.Form):
    confirm_code = forms.CharField(required=True, label='code', widget=forms.NumberInput,
                                   help_text='A code has been sent to the email you provided! <br> check and supply it here')
    
class PasswordEdit(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)