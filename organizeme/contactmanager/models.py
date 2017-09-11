from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Contact(models.Model):

    LOCATION_CHOICES = (("HOME","home"),("WORK", "work"))
    HOME = "HOME"
    WORK = "WORK"
    name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(blank=True)
    email_type = models.CharField(max_length=4, choices=LOCATION_CHOICES, default="HOME")
    address = models.CharField(max_length=30, null=True, blank=True)
    phone_number = models.CharField(max_length=19)
    phone_type = models.CharField(max_length=4, choices=LOCATION_CHOICES, default="HOME")
    image = models.ImageField(upload_to='contactPictures', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'contact'

    def __unicode__(self):
        return '%s  lives on %s' % (self.name, self.address)

    def __str__(self):
        return '%s lives on %s' % (self.name, self.address)
