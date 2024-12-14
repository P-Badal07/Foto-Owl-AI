from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Book Model
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)  # Unique ISBN for each book
    available = models.BooleanField(default=True)  # Availability status

    def __str__(self):
        return f"{self.title} by {self.author}"

# Borrow Request Model
class BorrowRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Denied', 'Denied'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Request by {self.user.username} for {self.book.title}"

# Borrow History (Archived Records)
class BorrowHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_on = models.DateField(default=timezone.now)
    returned_on = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"History: {self.user.username} borrowed {self.book.title}"
