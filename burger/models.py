from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, default='')
    views = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=128, unique=False, default="")
    desc = models.CharField(max_length=128, unique=False)
    picture = models.ImageField(upload_to='restaurant_images', blank=True)
    # lat = models.CharField(max_length=10, unique=False, help_text="Latitude", default="")
    # lon = models.CharField(max_length=10, unique=False, help_text="Longitude", default="")
    # categoryID = models.OneToOneField(Category)

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return (self.name + " " + self.desc)

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.title

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

class PointOfInterest(models.Model):
    name = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    position = GeopositionField(blank=True)
    restaurant = models.OneToOneField(Restaurant, null=True)

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'points of interest'

class BurgerCategories(models.Model):
    name = models.CharField(max_length=128, unique=True)
    def __unicode__(self):
        return self.name


class Burgers(models.Model):
    name = models.CharField(max_length=128, help_text="Burger Name")
    category = models.ForeignKey(BurgerCategories, null=True, help_text="Category")
    location = models.ForeignKey(PointOfInterest, null=True, help_text="Location")
    worst = models.BooleanField(default=False)
    best = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class Comments(models.Model):
    text = models.CharField(max_length=256, help_text="Insert comment")
    userID = models.OneToOneField(UserProfile)
    target = models.OneToOneField(Burgers)
    date = models.DateTimeField(auto_now_add=True, blank=True)
