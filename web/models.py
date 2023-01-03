from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


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
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)
    icon = models.ImageField(upload_to='categories/icons', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('single_category', kwargs={
            'slug': self.slug
        })


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('single_tag', kwargs={
            'slug': self.slug
        })


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
    hashtags = models.CharField(max_length=300, null=True, blank=True)
    like_score = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single_tutorial', kwargs={
            'slug': self.slug
        })


class Subscriber(models.Model):
    email = models.EmailField(null=False, blank=False)

    def __str__(self):
        return str(self.email)


class Feedback(models.Model):
    text = models.TextField(null=True, blank=True)
    tutorial = models.ForeignKey(Tutorial, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,  null=True, blank=True)


class UserTutorials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    category = models.CharField(max_length=20)
    additional_data = models.TextField()
    tutorial = models.ForeignKey(Tutorial, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username) + "'s tutorials."
