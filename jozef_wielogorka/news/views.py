from django.shortcuts import render
from django.core.mail import EmailMessage
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import News
from .forms import ContactForm


# Create your views here.
def home(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email_address = form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            email_1 = EmailMessage(
                "Nowa wiadomość",
                message,
                to=["jozek@wielomiod.pl"],
                from_email=email_address,
            )
            email_1.send()
            message = f"Hej {name},\nOtrzymałem Twoją prośbę o kontakt. Dziękuję ! Postaram się odpowiedzieć w ciągu najbliższych 72 godzin.\n\nPozdrawiam,\nJózek Wielogorka"
            email_2 = EmailMessage(
                "Contact request sent",
                message,
                to=[email_address],
            )
            email_2.send()
            messages.success(request, "Your message has been sent.")
            return HttpResponseRedirect("/#")
        else:
            messages.error(request, "Unsuccessful, please try again.")
    form = ContactForm()
    current = News.objects.order_by("-id").first()
    context = {
        "form": form,
        "news": current,
    }
    return render(request, "index.html", context)
