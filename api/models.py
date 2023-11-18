from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timedelta
# Create your models here.


class Auther(models.Model):
    name = models.CharField(max_length=50)
    biography = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    auther = models.ForeignKey(
        Auther, related_name='auther_books', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=350, null=True)
    available = models.IntegerField(
        default=0, validators=[MinValueValidator(0)])
    pages = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    publication_date = models.DateTimeField(
        null=True, blank=True, auto_now_add=True)

    def no_of_rate(self):
        return Rating.objects.filter(book=self).count()

    def avg_rate(self):
        ratings = Rating.objects.filter(book=self)
        avg_rate = 0
        count = self.no_of_rate()
        for rate in ratings:
            avg_rate += rate.rate
        return avg_rate / count if count > 0 else 0

    def __str__(self):
        return self.title


class Borrow(models.Model):
    user = models.ForeignKey(
        User, related_name='user_books', on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE)
    time = models.DateField(auto_now=True)

    def check_end(self):
        end_date = self.time + timedelta(days=7)
        # user passed the return date
        if datetime.now() > end_date:
            get_borrow = Borrow.objects.get(
                user=self,
                book=self
            )
            if get_borrow is not None:
                get_borrow.delete()

    def __str__(self):
        return self.book.title


class Rating(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, related_name='rating', on_delete=models.CASCADE)
    rate = models.IntegerField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return self.book.title

    class Meta:
        unique_together = (('user', 'book'))
        index_together = (('user', 'book'))
        ordering = ['rate']
