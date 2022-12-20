from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User as CustomUser
from django.core.mail import send_mail
from .forms import ContactForm
from rest_framework import viewsets
from .serializers import *
from rest_framework.exceptions import status
from rest_framework.response import Response
from .ai import create_tutorial
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
import json


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, **kwargs):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None, **kwargs):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, **kwargs):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)


def subscribe(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        email = data['email']
        s = Subscriber.objects.create(email=email)
        s.save()
        return JsonResponse({"subscribed": 'true'})


class TutorialViewSet(viewsets.ModelViewSet):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    permission_classes = [IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


def index(request):
    queryset = Technology.objects.all().order_by('name')
    work = WorkExperience.objects.all()
    item = Item.objects.all().order_by('id')
    team = Team.objects.all().order_by('name')

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            subject = 'You have a contact'
            from_email = 'dev.jum.mk'
            content = form.cleaned_data['name'] + '\n' + form.cleaned_data['email'] + '\n' + form.cleaned_data[
                'content']
            send_mail(
                subject,
                content,
                from_email,
                ['anovski3@gmail.com', 'dev.jum.mk'],
                fail_silently=True,
            )
            return redirect('index')
    else:
        form = ContactForm()
    context = {'item': queryset, 'work': work, 'team': team, 'items': item, 'form': form}
    return render(request, template_name='home.html', context=context)


def tutorials(request):
    if request.method == 'GET' and 'instant_search' in request.GET:
        tuts = Tutorial.objects.filter(title__contains=request.GET['instant_search'])
        return render(request, 'tutorials.html', context={'tuts': tuts})

    # Get all Tutorial objects with duplicate titles
    else:
        tuts = Tutorial.objects.all()[::-1]

        return render(request, 'tutorials.html', context={'tuts': tuts})


def single_tag(request, name=None):
    if request.method == 'GET' and 'instant_search' in request.GET:
        tuts = Tutorial.objects.filter(title__contains=request.GET['instant_search'])
        return render(request, 'tutorials.html', context={'tuts': tuts})
    else:
        tuts = Tutorial.objects.filter(tags__name__iexact=name)

        return render(request, 'tutorials/single_tag.html', context={'tuts': tuts, 'tag': name})


def single_category(request, name=None):
    if request.method == 'GET' and 'instant_search' in request.GET:
        tuts = Tutorial.objects.filter(title__contains=request.GET['instant_search'])
        return render(request, 'tutorials.html', context={'tuts': tuts})
    else:
        tuts = Tutorial.objects.filter(category__name=name)

        return render(request, 'tutorials/single_category.html', context={'tuts': tuts, 'cat': name})


def single_tutorial(request, slug=None, ):
    obj = get_object_or_404(Tutorial, slug=slug)
    absolute_url = obj.get_absolute_url()
    print(absolute_url)
    return render(request, 'tutorials/single_tutorial.html', context={'tutorial': obj})


def create(request):
    titles = [
        "How to Deploy Django on Amazon Web Services (AWS)",
        "How to Deploy Django on Google Cloud Platform (GCP)",
        "How to Deploy Django on Microsoft Azure",
        "How to Deploy Django on Heroku",
        "How to Deploy Django on DigitalOcean",
        "How to Deploy Django on Linode",
        "How to Deploy Django on Vultr",
        "How to Deploy Django on IBM Cloud",
        "How to Deploy Django on Oracle Cloud",
        "How to Deploy Django on Oracle Cloud Exadata",
        "How to Deploy Django on Oracle Cloud Autonomous",
        "How to Deploy Django on Oracle Cloud ATP",
        "How to Deploy Django on Oracle Cloud ADW",
        "How to Deploy Django on Rackspace Cloud",
        "How to Deploy Django on CloudSigma",
        "How to Deploy Django on CloudSigma Cloud",
        "How to Deploy Django on Interoute Cloud",
        "How to Deploy Django with React",
        "How to Deploy Django with Angular",
        "How to Deploy Django with Vue.js",
        "How to Deploy Django with Svelte",
        "How to Deploy Django with Next.js",
        "How to Deploy Django with Gatsby",
        "How to Deploy Django with Nuxt.js",
        "How to Deploy Django with Ember.js",
        "How to Deploy Django with Flutter",
        "How to Deploy Django with Xamarin",
        "How to Deploy Django with Ionic",
        "How to Deploy Django with Cordova",
        "How to Deploy Django with PhoneGap",
        "How to Deploy Django with NativeScript",
        "How to Deploy Django with Electron",
        "How to Deploy Django with Jest",
        "How to Deploy Django with Mocha",
        "How to Deploy Django with Jest",
        "How to Deploy Django with Chai",
        "How to Deploy Django with Enzyme",
        "How to Use Django with React",
        "How to Use Django with Angular",
        "How to Use Django with Vue.js",
        "How to Use Django with Svelte",
        "How to Use Django with Next.js",
        "How to Use Django with Gatsby",
        "How to Use Django with Nuxt.js",
        "How to Use Django with Ember.js",
        "How to Use Django with Flutter",
        "How to Use Django with Xamarin",
        "How to Use Django with Ionic",
        "How to Use Django with Cordova",
        "How to Use Django with PhoneGap",
        "How to Use Django with NativeScript",
        "How to Use Django with Electron",
        "How to Use Django with Jest",
        "How to Use Django with Mocha",
        "How to Use Django with Jest",
        "How to Use Django with Chai",
        "How to Use Django with Enzyme"]
    for x in titles:
        try:
            create_tutorial(x, 'Django')
        except:
            print('Failed to create')
    return HttpResponse(request, 'Done')


def delete_duplicates():
    tutorials = Tutorial.objects.values('title').annotate(Count('title')).order_by().filter(title__count__gt=1)

    # Loop through the Tutorial objects and delete the ones that are duplicates
    for tutorial in tutorials:
        title = tutorial['title']
        tutorials_with_title = Tutorial.objects.filter(title=title)
        # Keep the first Tutorial object and delete the others
        first_tutorial = tutorials_with_title.first()
        tutorials_to_delete = tutorials_with_title.exclude(pk=first_tutorial.pk)
        tutorials_to_delete.delete()

    return None
