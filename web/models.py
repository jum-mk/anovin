from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse


class Link(models.Model):
    link = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TechnologyItem(models.Model):
    name = models.CharField(max_length=255)
    link = models.ForeignKey(Link, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Technology(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='technology_icons')
    item = models.ManyToManyField(TechnologyItem)

    def __str__(self):
        return self.name


class WorkExperience(models.Model):
    company = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to='clients', blank=True, null=True)
    role = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.company


class Team(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='technology_icons')
    job = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='technology_icons')
    name_2 = models.CharField(max_length=255)
    link = models.URLField(max_length=255)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=255)
    content = models.TextField(max_length=300)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Tag(models.Model):
    objects = None
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tutorial(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=225, null=True, blank=True)
    meta_description = models.TextField()
    introduction = models.TextField()
    steps = models.TextField()
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    img = models.ImageField(upload_to='tutorials/images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single_tutorial', kwargs={
            'slug': self.slug
        })
