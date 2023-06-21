from django.contrib.auth import get_user_model
from django.db import models

Author = get_user_model()


class Book(models.Model):
    title = models.CharField(null=False, blank=False, max_length=255)
    author = models.ForeignKey(
        Author,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="books",
    )
    publication_date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title


class Page(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="pages")
    number = models.IntegerField()
    content = models.TextField()

    def __str__(self):
        return f"Page {self.number} of {self.book.title}"
