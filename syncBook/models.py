from django.db import models

# Create your models here.

class Add_book_from_user(models.Model):
    book_name = models.CharField(max_length=20)
    book_author = models.CharField(max_length=10)
    type_of_book = models.CharField(max_length=10)
    submit_from = models.CharField(max_length=10)

    def __str__(self):
        return self.book_name


class Update_book(models.Model):
    book_name = models.CharField(max_length=20)
    book_author = models.CharField(max_length=10)
    book_intro = models.TextField()
    book_cover_link = models.CharField(max_length=512)

    def __str__(self):
        return self.book_name


class Books(models.Model):
    book_name = models.CharField(max_length=20)
    book_author = models.CharField(max_length=10)
    book_intro = models.TextField()
    book_cover_link = models.CharField(max_length=512)
    type_of_book = models.CharField(max_length=10)

    def __str__(self):
        return self.book_name


