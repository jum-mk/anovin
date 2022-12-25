from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User as CustomUser
from django.core.mail import send_mail
from .forms import ContactForm
from rest_framework import viewsets
from .serializers import *
from rest_framework.exceptions import status
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
import json
from .aiv2 import create_tutorial as c_tut
from openai.error import ServiceUnavailableError


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
            from_email = 'anovski3@gmail.com'
            content = form.cleaned_data['name'] + '\n' + form.cleaned_data['email'] + '\n' + form.cleaned_data[
                'content']
            send_mail(
                subject,
                content,
                from_email,
                ['anovski3@gmail.com'],
                fail_silently=False,
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
    # djuma = [
    #     "How to Use Best Practices in Software Security",
    #     "How to Implement Secure Software Development Practices",
    #     "How to Follow Best Practices for Software Security",
    #     "How to Secure Your Software Development Process",
    #     "How to Improve Your Software Security Skills",
    #     "How to Master Software Security Principles",
    #     "How to Enhance Your Software Security Workflow",
    #     "How to Adhere to Best Practices in Software Security",
    #     "How to Apply Software Security Best Practices",
    #     "How to Become a Software Security Best Practices Expert"
    # ]
    titles = [
        "How to Install HTMX",
        "How to Use HTMX for Web Development",
        "How to Use HTMX for HTML Templates",
        "How to Use HTMX for Component-Based Development",
        "How to Use HTMX for Reusable Components",
        "How to Use HTMX for HTML Imports",
        "How to Use HTMX for Data Binding",
        "How to Use HTMX for Event Handling",
        "How to Use HTMX for Form Validation",
        "How to Use HTMX for Responsive Design",
        "How to Use HTMX for Accessibility",
        "How to Use HTMX for Internationalization",
        "How to Use HTMX for Server-Side Rendering",
        "How to Use HTMX for Progressive Web Apps",
        "How to Use HTMX for Hybrid Mobile Apps",
        "How to Use HTMX for Web Components",
        "How to Use HTMX for Custom Elements",
        "How to Use HTMX for Shadow DOM",
        "How to Use HTMX for Templates and Slots",
        "How to Use HTMX for HTML Parsing and Serialization",
        "How to Use HTMX for DOM Manipulation",
        "How to Use HTMX for Polyfills and Fallbacks",
        "How to Use HTMX for Compatibility and Interoperability",
        "How to Use HTMX for Debugging and Testing",
        "How to Use HTMX for Performance Optimization",
        "How to Use HTMX for Security Best Practices",
        "How to Use HTMX for Deployment and Hosting",
        "How to Use HTMX for Collaboration and Version Control",
        "How to Use HTMX for Continuous Integration and Deployment",
        "How to Use HTMX for Documentation and Tutorials",
        "How to Use HTMX for Community and Support",
        "How to Use HTMX for Code Reuse and Sharing",
        "How to Use HTMX for Package Management and Dependencies",
        "How to Use HTMX for Build Tools and Task Automation",
        "How to Use HTMX for Code Quality and Linting",
        "How to Use HTMX for Code Formatting and Style Guides",
        "How to Use HTMX for Code Refactoring and Maintenance",
        "How to Use HTMX for Code Review and Feedback",
        "How to Use HTMX for Codebase Architecture and Design",
        "How to Use HTMX for Codebase Scalability and Sustainability", ]
    # tutorials = Tutorial.objects.filter(hashtags=None)
    # for t in tutorials:
    #     print(t.hashtags)
    #     while True:
    #         try:
    #             title = str(t.title)
    #             hashtags = str(get_ai_text('Give me 8 hashtags for my blog post with title: {0}.'.format(title), 512))
    #             t.hashtags = hashtags
    #             print(t.hashtags)
    #             t.save()
    #
    #         except ServiceUnavailableError:
    #             continue
    #         break
    for title in titles:

        try:
            Tutorial.objects.get(title=title.replace('?', ''))
            print('Tutorial already exists')
        except:
            print(title)
            c_tut(title.replace('?', '  '), 'Web development')

    # consumer_key = "9kVtqWzkL6YN2vBHpRGzgYRDF"
    # consumer_secret = "foNH1CuPH7OJZPjpmlWGkK88XTPYJmLiXwQoTpmnwha0rUFjg4"
    # access_token = "792894589514485760-M8rkmQicexNh1BRdRtyrEQd5mtI2ScQ"
    # access_token_secret = "vtVZxmQPC7uhJJYT0fCzU8zhNDthVgRJZzJlYu6aBWpys"

    # auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    # api = tweepy.API(auth)

    # api.update_status('This is a tweet posted using Python and the tweepy library!')
    return HttpResponse(request, 'Done')


def delete_duplicates(request):
    tutorials = Tutorial.objects.values('slug').annotate(Count('slug')).order_by().filter(slug__count__gt=1)

    # Loop through the Tutorial objects and delete the ones that are duplicates
    for tutorial in tutorials:
        title = tutorial['slug']
        tutorials_with_title = Tutorial.objects.filter(slug=title)
        # Keep the first Tutorial object and delete the others
        first_tutorial = tutorials_with_title.first()
        tutorials_to_delete = tutorials_with_title.exclude(pk=first_tutorial.pk)
        tutorials_to_delete.delete()

    return HttpResponse('ok')
