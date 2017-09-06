from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Contact

class EditForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['image', 'name', 'email', 'email_type', 'address',
                  'phone_type', 'phone_number']

    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'name': 'image'}))
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'name'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'name': 'email'}))
    email_type = forms.ChoiceField(choices = Contact.LOCATION_CHOICES, label="", initial=Contact.HOME, widget=forms.Select(attrs={'class': 'form-control', 'name': 'email_type'}), required=False)
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'address'}))
    phone_type = forms.ChoiceField(choices = Contact.LOCATION_CHOICES, label="", initial=Contact.HOME, widget=forms.Select(attrs={'class': 'form-control', 'name': 'phone_type'}), required=False)
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'phone_number'}))

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['image', 'name', 'email', 'email_type', 'address',
                  'phone_type', 'phone_number']
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'name': 'image'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'name': 'email'}))
    email_type = forms.ChoiceField(choices = Contact.LOCATION_CHOICES, label="", initial=Contact.HOME, widget=forms.Select(attrs={'class': 'form-control', 'name': 'email_type'}), required=True)
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'address'}))
    phone_type = forms.ChoiceField(choices = Contact.LOCATION_CHOICES, label="", initial=Contact.HOME, widget=forms.Select(attrs={'class': 'form-control', 'name': 'phone_type'}), required=True)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'phone_number'}))

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'confirm_password'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'name': 'email'}))

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        if str(password) != str(confirm_password) and password and confirm_password:
            raise forms.ValidationError('The passwords do not match.')

        try:
            user = User.objects.filter(username=username)

            if user:
                raise forms.ValidationError('The username entered is already taken.')

        except User.DoesNotExist:
            return self.cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        try:
            user = authenticate(username=username, password= password)

            if user:
                return self.cleaned_data
                
        except User.DoesNotExist:
            raise forms.ValidationError('You entered the wrong password and username combination.')

        raise forms.ValidationError('You entered the wrong password and username combination.')
