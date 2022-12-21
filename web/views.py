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
from .aiv2 import create_tutorial as c_tut


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


def single_tag(request, slug=None):
    if request.method == 'GET' and 'instant_search' in request.GET:
        tuts = Tutorial.objects.filter(title__contains=request.GET['instant_search'])
        return render(request, 'tutorials.html', context={'tuts': tuts})
    else:
        tuts = Tutorial.objects.filter(tags__slug__iexact=slug)
        tag = Tag.objects.filter(slug=slug)[0]
        return render(request, 'tutorials/single_tag.html', context={'tuts': tuts, 'tag': tag, 'slug': slug})


def single_category(request, slug=None):
    if request.method == 'GET' and 'instant_search' in request.GET:
        tuts = Tutorial.objects.filter(title__contains=request.GET['instant_search'])
        return render(request, 'tutorials.html', context={'tuts': tuts})
    else:
        tuts = Tutorial.objects.filter(category__slug=slug)
        cat = Category.objects.filter(slug=slug)[0]
        return render(request, 'tutorials/single_category.html', context={'tuts': tuts, 'slug': slug, 'cat': cat})


def single_tutorial(request, slug=None):
    obj = get_object_or_404(Tutorial, slug=slug)
    related_articles = Tutorial.objects.filter(category=obj.category)[:10]

    return render(request, 'tutorials/single_tutorial.html',
                  context={'tutorial': obj, 'related_tutorials': related_articles})


def create(request):
    titles = ["How do I use the Web Audio API to add audio capabilities to my web application?",
              "How do I create and use custom templates in a Django application?",
              "How do I use the Fetch API to make HTTP requests in my web application?",
              "How do I use the WebGL API to add 3D graphics to my web application?",
              "How do I create and use custom modules in a Node.js application?",
              "How do I use the WebRTC API to add real-time audio and video capabilities to my web application?",
              "How do I create and use custom widgets in a PyQt application?",
              "How do I use the Web Bluetooth API to connect to and interact with Bluetooth devices from my web application?",
              "How do I create and use custom skins in a DotNetNuke application?",
              "How do I use the WebHID API to interact with human interface devices (HIDs) from my web application?",
              "How do I create and use custom plugins in a Joomla application?",
              "How do I use the WebXR API to build virtual reality (VR) and augmented reality (AR) experiences in my web application?",
              "How do I create and use custom modules in a Drupal application?",
              "How do I use the Payment Request API to streamline the checkout process in my web application?",
              "How do I create and use custom components in a Svelte application?",
              "How do I use the Web Animations API to add rich animation effects to my web application?",
              "How do I create and use custom extensions in a Joomla application?",
              "How do I use the Web Speech API to add voice recognition and synthesis capabilities to my web application?",
              "How do I create and use custom add-ons in a ExpressionEngine application?",
              "How do I use the Web NFC API to read and write NFC tags from my web application?",
              "How do I create and use custom plugins in a Magento application?",
              "How do I use the Resize Observer API to track element size changes in my web application?",
              "How do I use the Push API to send push notifications to users of my web application?",
              "How do I create and use custom templates in a Kirby application?",
              "How do I use the Server-Timing API to add performance metrics to my web application?",
              "How do I create and use custom modules in a Concrete5 application?",
              "How do I use the WebAuthn API to add strong authentication capabilities to my web application?",
              "How do I create and use custom plugins in a Shopify application?",
              "How do I use the Web Assembly System Interface (WASI) to access system functions from my web application?",
              "How do I create and use custom extensions in a VirtueMart application?",
              "How do I use the WebAssembly Threads API to add multithreading capabilities to my web application?",
              "How do I create and use custom templates in a Textpattern application?",
              "How do I use the WebAssembly SIMD API to add single instruction, multiple data (SIMD) capabilities to my web application?",
              "How do I create and use custom widgets in a Zend Framework application?",
              "How do I use the WebAssembly Reference Types API to add references and pointers to my web assembly code?",
              "How do I create and use custom modules in a MODX application?",
              "How do I use the WebAssembly GC API to add garbage collection capabilities to my web assembly code?",
              "How do I create and use custom plugins in a WooCommerce application?",
              "How do I use the WebAssembly Exceptions API to add exception handling capabilities to my web assembly code?",
              "How do I create and use custom extensions in an OpenCart application?",
              "How do I use the WebAssembly Table API to add tables and arrays to my web assembly code?",
              "How do I create and use custom modules in a BigCommerce application?",
              "How do I use the WebAssembly Multi-Value API to return multiple values from functions in my web assembly code?",
              "How do I create and use custom plugins in a PrestaShop application?",
              "How do I use the WebAssembly Memory API to add dynamic memory allocation capabilities to my web assembly code?",
              "How do I create and use custom extensions in a Magento 2 application?",
              "How do I use the WebAssembly Text Decoding API to decode text from different encoding formats in my web assembly code?",
              'How do I use the Push API to send push notifications to users of my web application?',
              'How do I create and use custom templates in a Kirby application?',
              'How do I use the Server-Timing API to add performance metrics to my web application?',
              'How do I create and use custom modules in a Concrete5 application?',
              'How do I use the WebAuthn API to add strong authentication capabilities to my web application?',
              'How do I create and use custom plugins in a Shopify application?',
              'How do I use the Web Assembly System Interface (WASI) to access system functions from my web application?',
              'How do I create and use custom extensions in a VirtueMart application?',
              'How do I use the WebAssembly Threads API to add multithreading capabilities to my web application?',
              'How do I create and use custom templates in a Textpattern application?',
              'How do I use the WebAssembly SIMD API to add single instruction, multiple data (SIMD) capabilities to my web application?',
              'How do I create and use custom widgets in a Zend Framework application?',
              'How do I use the WebAssembly Reference Types API to add references and pointers to my web assembly code?',
              'How do I create and use custom modules in a MODX application?',
              'How do I use the WebAssembly GC API to add garbage collection capabilities to my web assembly code?',
              'How do I create and use custom plugins in a WooCommerce application?',
              'How do I use the WebAssembly Exceptions API to add exception handling capabilities to my web assembly code?',
              'How do I create and use custom extensions in an OpenCart application?',
              'How do I use the WebAssembly Table API to add tables and arrays to my web assembly code?',
              'How do I create and use custom modules in a BigCommerce application?',
              'How do I use the WebAssembly Multi-Value API to return multiple values from functions in my web assembly code?',
              'How do I create and use custom plugins in a PrestaShop application?',
              'How do I use the WebAssembly Memory API to add dynamic memory allocation capabilities to my web assembly code?',
              'How do I create and use custom extensions in a Magento 2 application?',
              'How do I use the WebAssembly Text Decoding API to decode text from different encoding formats in my web assembly code?',
              'How do I use version control effectively for web development projects?',
              'How do I set up a staging environment for testing new features and changes before deploying them to production?',
              'How do I use Git efficiently for web development projects?',
              'How do I integrate third-party APIs into my web application?',
              'How do I set up a load balancer to improve the scalability of my web application?',
              'How do I use npm effectively for managing dependencies in my web project?',
              'How do I set up a continuous integration and delivery pipeline for a serverless application?',
              'How do I implement passwordless authentication in my web application?',
              'How do I create and use custom middleware in a Express.js application?',
              'How do I set up and use a database for my web application?',
              'How do I use JSON Web Tokens (JWTs) to handle authentication in my web application?',
              'How do I create and use custom directives in a Angular application?',
              'How do I use Webpack effectively to bundle and optimize my web application?',
              'How do I implement real-time updates using Server-Sent Events (SSE)?',
              'How do I create and use custom plugins in a WordPress application?',
              'How do I set up and use a content delivery network (CDN) for my web application?',
              'How do I use Firebase to add real-time capabilities to my web application?',
              'How do I create and use custom filters in a Vue.js application?',
              'How do I use GraphQL to build a flexible and efficient API for my web application?',
              'How do I set up and use a object storage service, such as Amazon S3, for my web application?',
              'How do I use WebAssembly to improve the performance of my web application?',
              'How do I create and use custom elements in a Polymer application?',
              'How do I use the Service Worker API to build a progressive web application (PWA)?',
              'How do I create and use custom behaviors in a Riot application?',
              'How do I use the IndexedDB API to store data in the browser for offline use?',
              'How do I create and use custom macros in a Blade application?']

    for title in titles:
        try:
            Tutorial.objects.get(title=x)
            print('Already exists')
        except:
            c_tut(title, 'WEB APIs')
            print('FINISH --------------------- FINISH ---------------------')

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
