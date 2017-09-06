from django.contrib import admin
from contactmanager.models import Contact

# change the way the information is viewed in admin.
class ContactAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'phone_number', 'phone_type', 'email', 'email_type']
    class Meta:
        model = Contact

# Register your models here.
admin.site.register(Contact, ContactAdmin)
