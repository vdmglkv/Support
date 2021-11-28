from django_choice import DjangoChoice, DjangoChoices


class StatusChoice(DjangoChoices):
    RESOLVED = DjangoChoice('Resolved')
    UNRESOLVED = DjangoChoice('Unresolved')
    FROZEN = DjangoChoice('Frozen')
