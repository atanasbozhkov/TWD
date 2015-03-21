from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=128, unique=False)
    location = models.CharField(max_length=512, unique=False)
    desc = models.CharField(max_length=128, unique=False)
    categoryID = models.OneToOneField(Category)

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return (self.name + " " + self.desc)