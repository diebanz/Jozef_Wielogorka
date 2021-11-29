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
            msg = form.cleaned_data['message']
            email_1 = create_mail_to_owner(msg, email_address, name)
            email_1.send()
            message = f"Hej {name},\nOtrzymałem Twoją prośbę o kontakt. Dziękuję ! Postaram się odpowiedzieć w ciągu najbliższych 72 godzin.\n\nPozdrawiam,\nJózek Wielogorka"
            email_2 = EmailMessage(
                'Contact request sent',
                message,
                to=[email_address],
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
    current = News.objects.order_by('-id').first()
    context = {
        'form': form,
        'news': current,
    }
    return render(request, 'index.html', context)


def create_mail_to_owner(msg, target, target_name):
    special_characters = {
        ' ': '%20',
        '!': '%21',
        '"': '%22',
        '#': '%23',
        '$': '%24',
        '%': '%25',
        '&': '%26',
        '\'': '%27',
        '(': '%28',
        ')': '%29',
        '*': '2A',
        '+': '2B',
        ',': '2C',
        '-': '2D',
        '.': '2E',
        '/': '2F',
        ':': '%3A',
        ';': '%3B',
        '<': '%3C',
        '=': '%3D',
        '>': '%3E',
        '?': '%3F',
        '[': '%5B',
        '\\': '%5C',
        ']': '%5D',
        '^': '%5E',
        '_': '%5F',
        '`': '%60',
        '{': '%7B',
        '|': '%7C',
        '}': '%7D',
        '~': '%7E',
        '€': '%E2%82%AC',
    }
    translation_table = msg.maketrans(special_characters)
    return EmailMessage(
                f'Nowa wiadomość na wielomiod.pl napisana przez {target}',
                f'Dzień dobry {target_name},\n\n\n' + f'mailto:{{{target}}}?subject={{Re%3AYour%20Request}}&{{{msg.translate(translation_table)}}}'',
                to=['jozek@wielomiod.pl'],
            )
