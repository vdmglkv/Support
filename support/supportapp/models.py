from django.db import models
from supportapp.choices import StatusChoice


class Ticket(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    from_user = models.CharField(max_length=255, default="Unknown")
    support_answer = models.CharField(max_length=255, default='None')
    user_answer = models.CharField(max_length=255, default='None')
    status = models.CharField(max_length=10, choices=StatusChoice.CHOICES, default=StatusChoice.UNRESOLVED)

    def __str__(self):
        return self.title
