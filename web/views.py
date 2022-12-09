from django.shortcuts import render, redirect
from .models import *
from django.core.mail import send_mail
from .forms import ContactForm


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
