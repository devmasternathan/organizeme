from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, render_to_response
from django.template import RequestContext
from django.views.generic import FormView, View
from django.db.models import Q
from .forms import ContactForm, EditForm, LoginForm, UserForm
from lazysignup.decorators import allow_lazy_user
from .models import Contact

# Create your views here.

def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

def home_view(request):
	 context = RequestContext(request)
	 data ={
		"is_authenticated": context.request.user.is_authenticated()
	 }
	 if data['is_authenticated']:
		 return redirect('organizeme:manager', slug=1)
	 else:
	 	return render(context.request, 'home.html', data)

def manager_view(request):
	context = RequestContext(request)

	data ={
		"is_authenticated": context.request.user.is_authenticated()
	}

	return render(context.request, 'manager.html', data)

def remove_view(request, id):
	 context = RequestContext(request)
	 err = None
	 try:
		 contact_item = Contact.objects.get(id=id)
		 contact_item.delete()
	 except ObjectDoesNotExist as error:
		 err = "contact does not exist: {0}".format(error)
	 data ={
		"is_authenticated": context.request.user.is_authenticated(),
		"error": err
	 }
	 return redirect('organizeme:manager', slug=1)

def logout_view(request):
	context = RequestContext(request)
	if context.request.user.is_authenticated():
		auth.logout(request)
	return redirect('organizeme:home')

class UserFormView(View):
	form_class = UserForm
	template_name = "register.html"

	def get(self, request):
		context = RequestContext(request)
		form = self.form_class(None)
		data ={
			"is_authenticated": context.request.user.is_authenticated(),
			'form':form,
			"error": None
		}
		return render(context.request, self.template_name, data)

	def post(self, request):
		context = RequestContext(request)
		form = self.form_class(context.request.POST)
		err = None

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
					login(context.request, user)
					return redirect('organizeme:manager', slug=1)
				else:
					err = 'user could not be authenticated.'
			except IntegrityError as e:
				if 'unique constraint' in e.args[0]:
					err += str(e.args) + ' '
					data ={
						"is_authenticated": context.request.user.is_authenticated(),
						'form':form,
						"error": err
					}
					return render(context.request, self.template_name, data)

		data ={
			"is_authenticated": context.request.user.is_authenticated(),
			'form':form,
			"error": err
		}
		return render(context.request, self.template_name, data)

class LoginFormView(View):
	form_class = LoginForm
	template_name = "login.html"

	# when user want this form get this
	# display blank form
	def get(self, request):
		context = RequestContext(request)
		form = self.form_class(None)
		data ={
			"is_authenticated": context.request.user.is_authenticated(),
			'form':form,
			'error': None
		}
		return render(context.request, self.template_name, data)

	# process form data
	def post(self, request):
		context = RequestContext(request)
		form = self.form_class(context.request.POST)
		err = None

		if form.is_valid():
			# get data that is formatted properly
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password= password)

			if user is not None:
				login(context.request, user)
				return redirect('organizeme:manager', slug=1)
			else:
				err = "Error: Your account could not be found. \
				Try again or contact us via 1-111-1111"

		data ={
			"is_authenticated": context.request.user.is_authenticated(),
			'form':form,
			'error': err
		}
		return render(context.request, self.template_name, data)

class ContactFormView(View):
	form_class = ContactForm
	template_name = "manager.html"

	def get(self, request, slug):
		context = RequestContext(request)
		form = self.form_class(None)
		page = context.request.GET.get('page', 1)
		query = context.request.GET.get('query')
		id = context.request.user.id
		err = None

		if query:
			contact_list =  Contact.objects.filter(user_id = id).filter(
				Q(name__icontains=query) |
				Q(email__icontains=query) |
				Q(address__icontains=query) |
				Q(phone_number__icontains=query) |
				Q(email_type__icontains=query) |
				Q(phone_type__icontains=query)
				).distinct().order_by('name')
		else:
			err = "This query produced no results. Please try another \
			word or clear the input and press enter to get all your contacts."
			contact_list = Contact.objects.filter(user_id=id).order_by('name')

		if page == 1:
			if slug is not None:
				page = slug

		paginator = Paginator(contact_list, 7)

		try:
			contact_list = paginator.page(page)
		except PageNotAnInteger as error:
			err = "contact does not exist: {0}".format(error)
			contact_list = paginator.page(1)
		except EmptyPage as error:
			err = "contact does not exist: {0}".format(error)
			contact_list = paginator.page(paginator.num_pages)

		data ={
			'is_authenticated': context.request.user.is_authenticated(),
			'form': form,
			'list': contact_list,
			'error' : err
		}
		return render(context.request, self.template_name, data)

	def post(self, request, slug):
		context = RequestContext(request)
		form = self.form_class(context.request.POST, context.request.FILES or None)
		err = None

		if form.is_valid():
			contact = form.save(commit=False)
			contact.user = context.request.user
			contact.save()
		else:
			err = 'error :  form submission failed. Please re-enter.'

		contact_list = Contact.objects.filter(user_id=context.request.user.id).order_by('name')
		paginator = Paginator(contact_list, 7)
		contact_list = paginator.page(1)

		data ={
			"is_authenticated": context.request.user.is_authenticated(),
			'form':form,
			'list': contact_list,
			'error': err
		}

		return render(context.request, self.template_name, data)

class EditFormView(View):
	form_class = EditForm
	template_name= "edit.html"

	def get(self, request, slug):
		context = RequestContext(request)
		form = self.form_class(None)
		exist = True
		contact_item = Contact.objects.get(id=slug)

		data ={
		"is_authenticated": context.request.user.is_authenticated(),
		"list_item": contact_item,
		"exist": exist,
		"form": form
		}
		return render(context.request, self.template_name, data)

	def post(self, request, slug):
		context = RequestContext(request)
		form = self.form_class(context.request.POST, context.request.FILES or None)

		if form.is_valid():
			contact = form.save(commit=False)
			contact_item = Contact.objects.get(id=slug)
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			email_type = form.cleaned_data['email_type']
			address = form.cleaned_data['address']
			phone_number = form.cleaned_data['phone_number']
			phone_type = form.cleaned_data['phone_type']
			image = form.cleaned_data['image']

			if name:
				contact_item.name = name
			if email:
				contact_item.email = email
			if email_type:
				contact_item.email_type = email_type
			if address:
				contact_item.address = address
			if phone_number:
				contact_item.phone_number = phone_number
			if phone_type:
				contact_item.phone_type = phone_type
			if image:
				contact_item.image = image

			contact_item.save()
			return redirect('organizeme:manager', slug=1)
			data ={
			"is_authenticated": context.request.user.is_authenticated(),
			"list_item": contact_item,
			"exist": exist,
			"form": form
			}
		return render(request, self.template_name, data)

@allow_lazy_user
def demo_view(request, slug):
	return redirect('organizeme:manager', slug=1)
