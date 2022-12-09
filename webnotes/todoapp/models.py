from django.db import models
from authapp.models import User

# Create your models here.


class Project(models.Model):
    name = models.CharField(verbose_name='project name', max_length=50, unique=True)
    repo_url = models.URLField(verbose_name='link to repository', blank=True)
    users = models.ManyToManyField(User, verbose_name="project participants")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Project_{self.name}'


class Todo(models.Model):
    TODO = 'TD'
    IN_PROGRESS = 'PR'
    IN_REVIEW = 'RW'
    CLOSED = 'CL'
    BLOCKED = 'BL'

    STATUS_CHOICES = [
        (TODO, 'to do'),
        (IN_PROGRESS, 'in progress'),
        (IN_REVIEW, 'in review'),
        (CLOSED, 'closed'),
        (BLOCKED, 'blocked')
    ]

    name = models.CharField(verbose_name='note title', max_length=50, blank=True)
    content = models.TextField(verbose_name='note content')
    publication_date = models.DateTimeField(auto_now=True)  # when updated
    by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='by_user')
    by_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='by_project')
    status = models.CharField(verbose_name='note status', max_length=2, choices=STATUS_CHOICES, default=TODO)

    def __str__(self):
        return f'{self.name}'
