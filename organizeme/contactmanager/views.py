from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserForm
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.contrib import auth
from django.views.generic import View
from django.shortcuts import redirect
from django.db import IntegrityError

# Create your views here.
def home_view(request):
     context ={
        "is_authenticated": request.user.is_authenticated()
     }
     return render(request, 'home.html', context)

def manager_view(request):
    context = RequestContext(request)
    context ={
        "is_authenticated": request.user.is_authenticated()
    }
    return render(request, 'manager.html', context)

def register_view(request):
    context ={
        "is_authenticated": request.user.is_authenticated()
    }
    return render(request, 'register.html', context)

def demo_view(request):
    context ={
        "is_authenticated": request.user.is_authenticated()
    }
    return render(request, 'manager.html', context)

def login_view(request):
    context ={
        "is_authenticated": request.user.is_authenticated()
    }
    return render(request, 'login.html', context)

def logout_view(request):
    context = RequestContext(request)

    #if you are logged in log out.
    if context.request.user.is_authenticated():
        auth.logout(request)

    return redirect('organizeme:home')


class UserFormView(View):
    form_class = UserForm
    template_name = "register.html"

    # when user want this form get this
    # display blank form
    def get(self, request):
        form = self.form_class(None)
        context ={
            "is_authenticated": request.user.is_authenticated(),
            'form':form
        }
        return render(request, self.template_name, context)

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            try:
                user = form.save(commit=False)
                # get data that is formatted properly
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user.set_password(password)
                user.save()

                user = authenticate(username=username, password= password)

                if user is not None:
                    login(request, user)
                    return redirect('organizeme:manager')
            except IntegrityError as e:
                if 'unique constraint' in e.args[0]:
                    return render(request, self.template_name, context)

        context ={
            "is_authenticated": request.user.is_authenticated(),
            'form':form
        }
        return render(request, self.template_name, context)

class LoginFormView(View):
    form_class = LoginForm
    template_name = "login.html"

    # when user want this form get this
    # display blank form
    def get(self, request):
        form = self.form_class(None)
        context ={
            "is_authenticated": request.user.is_authenticated(),
            'form':form
        }
        return render(request, self.template_name, context)

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            # get data that is formatted properly
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password= password)

            if user is not None:
                login(request, user)
                return redirect('organizeme:manager')
        context ={
            "is_authenticated": request.user.is_authenticated(),
            'form':form
        }
        return render(request, self.template_name, context)
