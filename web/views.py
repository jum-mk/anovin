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
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import JsonResponse
import json
from .aiv2 import create_tutorial as c_tut
from openai.error import ServiceUnavailableError
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.contrib.auth import logout


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /subscribe/",
        "Disallow: /register/",
        "Disallow: /login_view/",
        "Disallow: /logout_view/",
        "Disallow: /sitemap.xml",
        "Disallow: /delete_duplicates/",
        "Disallow: /ct_feedback/",
        "Disallow: /feedback/",
        "Disallow: /my_tutorials/",
        "Disallow: /my_tutorials/",
        "Disallow: /create_tutorial/",
        "Disallow: /get_social_media_posts/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

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
    # import requests
    # import xml.etree.ElementTree as ET

    # def check_sitemap_links(sitemap_url):
    #     # Download the sitemap XML
    #     sitemap_response = requests.get(sitemap_url)
    #     sitemap_xml = sitemap_response.text
    #
    #     # Parse the XML
    #     sitemap = ET.fromstring(sitemap_xml)
    #
    #     # Iterate over each link in the sitemap
    #     for link in sitemap.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
    #         url = link.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
    #         print(url)
    #         # Check the HTTP status code for the link
    #         response = requests.get(url)
    #         if response.status_code == 404:
    #             print(f'{url} returned a 404 status code')
    # check_sitemap_links('https://anovin.mk/sitemap.xml')

    # for t in Tutorial.objects.all():
    #     print(t.slug)
    #     t.slug = str(t.slug).replace("(", '')
    #     print(t.slug)
    #     t.save()
    #     print(t.slug)

    from .tests import tutorials_dict
    for x in tutorials_dict:
        category = x
        print(category)
        title_list = tutorials_dict[x]
        for title in title_list:
            try:
                Tutorial.objects.get(title=title.replace('?', ''))
                print('Tutorial already exists')
            except:
                print('Trying to create a new tutorial.')
                c_tut(title.replace('?', ''), category)

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


def delete_duplicatesdelete_duplicates(request):
    if request.user.is_authenticated and request.user.is_superuser:
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


# Create tutorial feature feedback
def ct_feedback(request):
    if request.method == 'POST':
        # Get the like value from the POST request body
        data = request.POST
        print(data)
        user = request.user
        instance = Feedback.objects.create(user=user, )
        feedback_text = data['feedback-text']

        # Process the like value and return a response
        return JsonResponse({'error': 'Invalid request method'})


@api_view(('GET', 'POST'))
def create_tutorial(request):
    if request.method == 'POST':
        data = request.data

        print(data)

        # Get the form data
        title = data['title']
        category = data['category']
        additional_data = data['additional_data']
        user = request.user

        created_instance = c_tut(title, category)
        # # Save the form data to the database
        tutorial = UserTutorials.objects.create(title=title, category=category, additional_data=additional_data,
                                                user=user, tutorial=created_instance)
        tutorial.save()
        html_message = '<h3>Your tutorial `<a> href="{1}">{0}</a>`is ready. Please provide feedback.</h3>'.format(
            str(tutorial.title), str(tutorial.get_absolute_url()))
        try:
            send_mail(
                'Subject here',
                'Your tutorial is ready!',
                'anovindooel@gmail.com',
                [user.email, 'anovski3@gmail.com'],
                html_message=html_message,
                fail_silently=True
            )
        except:
            print('Mail not sent _createtutorial view')
            pass

        # # Redirect to a success page
        return Response({'created': created_instance.get_absolute_url()}, status.HTTP_201_CREATED)

    else:
        # Render the form template
        return render(request, 'tutorials/create_tutorial.html')


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return Response({'success': 'User created successfully'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': 'Username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        data = request.data
        print(data)
        username = data.get('username')
        password = data.get('password')  # Note: the form has "email" as the name of the password field
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'success': 'Logged in successfully'}, status=200)
        else:
            return Response({'error': 'Invalid login credentials'}, status=401)
    else:
        return Response({'error': 'Invalid request method'}, status=405)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')


def my_tutorials(request):
    if request.user.is_authenticated:
        if request.method == 'GET' and 'instant_search' in request.GET:
            tuts = UserTutorials.objects.filter(title__contains=request.GET['instant_search'])
            return render(request, 'tutorials/my_tutorials.html', context={'tuts': tuts})
        else:
            tuts = UserTutorials.objects.filter(user=request.user)
            context = {'tuts': tuts}
            return render(request, 'tutorials/my_tutorials.html', context)
