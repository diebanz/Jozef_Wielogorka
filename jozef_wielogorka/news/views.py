from django.shortcuts import redirect, render
from django.core.mail import EmailMessage
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import News
from .forms import ContactForm


# Create your views here.
def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email_address = form.cleaned_data['email']
            message = form.cleaned_data['message']
            email_1 = EmailMessage(
                f'New message on <website> by {email_address}',
                message,
                to=['sebanzian@gmail.com'],
                from_email='System',
            )
            email_1.send()
            message = f"Hello {name},\n\nWe received your contact request, thank you for reaching out. We will try and answer within 72 hours.\n\nBest regards,\nJozef Wielogorka"
            email_2 = EmailMessage(
                'Contact request sent',
                message,
                to=[email_address],
                from_email='no_reply'
            )
            email_2.send()
            messages.success(
                request,
                'Your message has been sent.'
            )
            return HttpResponseRedirect('/#')
        else:
            messages.error(
                request,
                'Unsuccessful, please try again.'
            )
    form = ContactForm()
    current = News.objects.all().order_by('-id')[0]
    context = {
        'form': form,
        'news': current,
    }
    return render(request, 'index.html', context)
