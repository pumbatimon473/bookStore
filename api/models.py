from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    genre = models.CharField(max_length=20)
    published_date = models.DateField()
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.title + ' (' + self.author + ')'
    