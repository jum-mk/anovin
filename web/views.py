from django.shortcuts import render, redirect
from .models import *
from django.core.mail import send_mail
from .forms import ContactForm
from rest_framework import viewsets
from .serializers import *


class TutorialViewSet(viewsets.ModelViewSet):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


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
    tags = Tag.objects.all()
    cats = Category.objects.all()
    tuts = Tutorial.objects.all()
    return render(request, 'tutorials.html', context={'tags': tags, 'cats': cats, 'tuts': tuts})


def single_tutorial(request, pk=None):
    tutorial = Tutorial.objects.get(id=pk)
    return render(request, 'tutorials/single_tutorial.html', context={'tutorial': tutorial})


languages = ['Java', 'C', 'C++', 'Python', 'C#', 'JavaScript', 'PHP', 'Assembly', 'Ruby', 'Swift', 'Objective-C', 'Go',
             'Perl', 'Rust', 'Kotlin', 'Scala', 'Dart', 'Julia', 'R', 'TypeScript', 'VBA', 'Groovy', 'FORTRAN', 'Lisp',
             'Matlab', 'Ada', 'Haskell', 'Erlang', 'Elixir', 'F#']
