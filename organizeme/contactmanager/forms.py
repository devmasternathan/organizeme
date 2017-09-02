from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    vpassword = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    def clean(self):
        password = self.cleaned_data.get('password')
        vpassword = self.cleaned_data.get('vpassword')
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        if str(password) != str(vpassword) and password and vpassword:
            raise forms.ValidationError('The passwords do not match.')

        try:
            user = User.objects.filter(username=username)

            if user:
                raise forms.ValidationError('The username entered is already taken.')
        except User.DoesNotExist:
            return self.cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

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
