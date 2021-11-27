from django.db import models


class Ticket(models.Model):
    CHOICES = (('Resolved', 'resolved'),
               ('Unresolved', 'unresolved'),
               ('Frozen', 'frozen'))
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=300, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    from_user = models.CharField(max_length=255, default="Unknown")
    support_answer = models.CharField(max_length=255, default='None')
    user_answer = models.CharField(max_length=255, default='None')
    status = models.CharField(max_length=10, choices=CHOICES, default='Unresolved')

    def __str__(self):
        return self.title
