from django.db import models
from django import forms

from django.contrib.auth.models import User

# Create your models here.


class MainMenu(models.Model):
    item = models.CharField(max_length=200, unique=True)
    link = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.item


class Book(models.Model):
    name = models.CharField(max_length=200)
    web = models.URLField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    publishdate = models.DateField(auto_now=True)
    picture = models.FileField(upload_to='bookEx/static/uploads')
    pic_path = models.CharField(max_length=300, editable=False, blank=True)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    original_owner = models.ForeignKey(User, related_name='current_owner', blank=True, null=True,
                                      on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class Comment(models.Model):
    title = models.CharField(max_length=200)
    comment = models.CharField(max_length=2000)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class Favorite(models.Model):
        username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
        book_id = models.IntegerField(default=0)

        def __str__(self):
            return str(self.id)

class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return f"Shopping Cart for {self.user.username}"
