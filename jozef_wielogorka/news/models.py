from django.db import models
from datetime import datetime


# Create your models here.
class News(models.Model):
    class Meta:
        verbose_name_plural = "news"

    title = models.CharField(max_length=150)
    body = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} ({datetime.strftime(self.date, "%d/%b/%y")})'
