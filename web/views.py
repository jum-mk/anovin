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

tutorials_dict = {
    'Golang': [
        "How to Install and Set Up Go on Your Development Machine",
        "How to Write Your First Go Program",
        "How to Use Go's Built-in Concurrency Features",
        "How to Build and Deploy a Go Web Server",
        "How to Use Go's Testing Framework",
        "How to Use Go's JSON Support to Work with APIs",
        "How to Use Go's Database Support to Store Data",
        "How to Use Go's Goroutines and Channels for Parallelism",
        "How to Use Go's Reflect Package to Inspect Types at Runtime",
        "How to Use Go's Text and Template Packages to Generate Text Output",
        "How to Use Go's Built-in Cryptography Libraries",
        "How to Use Go's Profiling Tools to Improve Performance"
    ],
    'Computational biology': ["How to Install and Set Up MEGA on Your Computer",
                              "How to Use MEGA for DNA and Protein Sequence Alignment",
                              "How to Use MEGA for Phylogenetic Tree Reconstruction",
                              "How to Use MEGA for Molecular Evolution Analysis",
                              "How to Use MEGA for Molecular Clock Analysis",
                              "How to Use MEGA for Protein Structure Prediction",
                              "How to Use MEGA for Population Genetic Analysis",
                              "How to Use MEGA for Molecular Functional Analysis",
                              "How to Use MEGA for Gene Expression Analysis",
                              "How to Use MEGA for Comparative Genomics Analysis",
                              "How to Use MEGA for Molecular Sequence Data Management",
                              "How to Use MEGA for Biomedical Research"
                              ],
    'Video editing': [
        "How to Install and Set Up Vegas Pro on Your Computer",
        "How to Use Vegas Pro for Video Editing and Production",
        "How to Use Vegas Pro's Audio Editing and Mixing Features",
        "How to Use Vegas Pro's Special Effects and Compositing Tools",
        "How to Use Vegas Pro's Color Correction and Grading Features",
        "How to Use Vegas Pro's 3D Modeling and Animation Tools",
        "How to Use Vegas Pro's Titling and Text Animation Features",
        "How to Use Vegas Pro's Video Stabilization and Motion Tracking Tools",
        "How to Use Vegas Pro's Audio Syncing and Lip Sync Tools",
        "How to Use Vegas Pro's DVD and Blu-ray Authoring Features",
        "How to Use Vegas Pro's Advanced Editing Techniques",
        "How to Use Vegas Pro's Collaboration and Teamwork Features"
    ],
    'React': ["How to Set Up a React Development Environment",
              "How to Create a React App from Scratch",
              "How to Use React Components and Props",
              "How to Use React State and Lifecycle Methods",
              "How to Use React Forms and Events",
              "How to Use React Routing and Navigation",
              "How to Use React Hooks and Context",
              "How to Use React Fragments and Portals",
              "How to Use React Lazy Loading and Suspense",
              "How to Use React for Server-Side Rendering",
              "How to Use React for Mobile Development with React Native",
              "How to Use React for Animations and Transitions"],
    'Next.js': ["How to Set Up a Next.js Development Environment",
                "How to Create a Next.js App from Scratch",
                "How to Use Next.js for Server-Rendered React Apps",
                "How to Use Next.js for Static Site Generation",
                "How to Use Next.js for Serverless Functions",
                "How to Use Next.js for Routing and Navigation",
                "How to Use Next.js for Data Fetching and SSR",
                "How to Use Next.js for Code Splitting and Optimization",
                "How to Use Next.js for Server-Side Rendering in a Microservices Architecture",
                "How to Use Next.js for Serverless APIs and Microservices",
                "How to Use Next.js for Server-Rendered React Apps with TypeScript",
                "How to Use Next.js for Server-Rendered React Apps with GraphQL"],
    'Headless CMS': ["How to Choose the Right Headless CMS for Your Project",
                     "How to Set Up and Configure a Headless CMS",
                     "How to Use a Headless CMS for Content Management and Editing",
                     "How to Use a Headless CMS for Digital Asset Management",
                     "How to Use a Headless CMS for Multi-Language and Localization",
                     "How to Use a Headless CMS for User Management and Access Control",
                     "How to Use a Headless CMS for Version Control and Workflow",
                     "How to Use a Headless CMS for SEO Optimization",
                     "How to Use a Headless CMS for Personalization and Targeting",
                     "How to Use a Headless CMS for Integration with External Systems",
                     "How to Use a Headless CMS for Webhooks and Event Triggers",
                     "How to Use a Headless CMS for Scalability and Performance"],
    'AJAX': ["How to Use AJAX for Asynchronous Web Applications",
             "How to Use AJAX with jQuery for Easier Web Development",
             "How to Use AJAX with PHP for Server-Side Interaction",
             "How to Use AJAX with ASP.NET for Server-Side Interaction",
             "How to Use AJAX with Ruby on Rails for Server-Side Interaction",
             "How to Use AJAX with Python for Server-Side Interaction",
             "How to Use AJAX with Java for Server-Side Interaction",
             "How to Use AJAX with Node.js for Server-Side Interaction",
             "How to Use AJAX with AngularJS for Single-Page Applications",
             "How to Use AJAX with React for Single-Page Applications",
             "How to Use AJAX with Vue.js for Single-Page Applications",
             "How to Use AJAX with Webpack and Babel for Modern JavaScript Applications"],
    'tweepy': ["How to Use Tweepy for Twitter API Access in Python",
               "How to Use Tweepy for Twitter Streaming API in Python",
               "How to Use Tweepy for Twitter Search and Filtering in Python",
               "How to Use Tweepy for Twitter User Lookup and Information in Python",
               "How to Use Tweepy for Twitter Status Update and Tweeting in Python",
               "How to Use Tweepy for Twitter Direct Messages in Python",
               "How to Use Tweepy for Twitter Friendship and Follow Management in Python",
               "How to Use Tweepy for Twitter List Management in Python",
               "How to Use Tweepy for Twitter Favorites and Likes in Python",
               "How to Use Tweepy for Twitter Retweet and Quote Tweet in Python",
               "How to Use Tweepy for Twitter User Block and Mute Management in Python",
               "How to Use Tweepy for Twitter OAuth and Authentication in Python"],
    'OpenAI': ["How to Use OpenAI's GPT-3 for Natural Language Processing",
               "How to Use OpenAI's GPT-3 for Text Generation and Summarization",
               "How to Use OpenAI's GPT-3 for Translation and Language Modelling",
               "How to Use OpenAI's DALL-E for Image Generation and Style Transfer",
               "How to Use OpenAI's DALL-E for Text-to-Image Generation",
               "How to Use OpenAI's DALL-E for Audio Generation",
               "How to Use OpenAI's RoboSumo for Robot Control and Reinforcement Learning",
               "How to Use OpenAI's RoboSumo for Robotics Simulation and Training",
               "How to Use OpenAI's Gym for Reinforcement Learning and Control",
               "How to Use OpenAI's Gym for Robotics Simulation and Training",
               "How to Use OpenAI's Spinning Up for Deep Reinforcement Learning",
               "How to Use OpenAI's API for NLP, Computer Vision, and Robotics"]
}


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
        tuts = Tutorial.objects.all()[:50:-5]
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
    import requests
    import xml.etree.ElementTree as ET

    def check_sitemap_links(sitemap_url):
        # Download the sitemap XML
        sitemap_response = requests.get(sitemap_url)
        sitemap_xml = sitemap_response.text

        # Parse the XML
        sitemap = ET.fromstring(sitemap_xml)

        # Iterate over each link in the sitemap
        for link in sitemap.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            url = link.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
            print(url)
            # Check the HTTP status code for the link
            response = requests.get(url)
            if response.status_code == 404:
                print(f'{url} returned a 404 status code')
    check_sitemap_links('https://anovin.mk/sitemap.xml')

    # for t in Category.objects.all():
    #     print(t.slug)
    #     t.slug = str(t.slug).replace("(", '')
    #     print(t.slug)
    #     t.save()
    #     print(t.slug)
    # from .tests import tutorials_dict
    # for x in tutorials_dict:
    #     category = x
    #     print(category)
    #     title_list = tutorials_dict[x]
    #     for title in title_list:
    #         try:
    #             Tutorial.objects.get(title=title.replace('?', ''))
    #             print('Tutorial already exists')
    #         except:
    #             print('Trying to create a new tutorial.')
    #             c_tut(title.replace('?', ''), category)

    # consumer_key = "9kVtqWzkL6YN2vBHpRGzgYRDF"
    # consumer_secret = "foNH1CuPH7OJZPjpmlWGkK88XTPYJmLiXwQoTpmnwha0rUFjg4"
    # access_token = "792894589514485760-M8rkmQicexNh1BRdRtyrEQd5mtI2ScQ"
    # access_token_secret = "vtVZxmQPC7uhJJYT0fCzU8zhNDthVgRJZzJlYu6aBWpys"

    # auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    # api = tweepy.API(auth)

    # api.update_status('This is a tweet posted using Python and the tweepy library!')

    # from celery import Celery
    # app = Celery('my_app')
    # app.config_from_object('celeryconfig')
    # if __name__ == '__main__':
    #     app.start()
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


def feedback(request):
    if request.method == 'POST':
        # Get the like value from the POST request body
        data = request.POST
        print(data)

        tutorial_id = data['tutorial_id']
        feedback_text = data['feedback-text']

        # Process the like value and return a response
        if feedback_text:
            tut = Tutorial.objects.get(id=int(tutorial_id))

            feedback_instance = Feedback.objects.create(text=feedback_text, tutorial=tut)
            feedback_instance.save()
            return JsonResponse({'message': 'Thanks for the feedback!'})
        else:
            return JsonResponse({'message': 'Thanks for the feedback!'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
