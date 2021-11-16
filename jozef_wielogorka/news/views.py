from django.shortcuts import render

from .models import News


# Create your views here.
def home(request):
    current = News.objects.all().order_by('-id')[0]
    context = {
        'news': current,
    }
    return render(request, 'index.html', context)
