from django.db import models

DONE = True
TODO = False
STATUS = (
        (DONE, 'Done'),
        (TODO, 'Not done'),
    )


class Project(models.Model):
    color = models.CharField(max_length=20, default='red')
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='projects')
    project_name = models.CharField(max_length=100)

    def __str__(self):
        return self.project_name


class Task(models.Model):

    HIGH = 0
    MIDDLE = 1
    LOW = 2
    PRIORITY = (
        (HIGH, 'red'),
        (MIDDLE, 'orange'),
        (LOW, 'white'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    task = models.CharField(max_length=300)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS)
    priority = models.CharField(max_length=10, choices=PRIORITY)

    class Meta:
        ordering = ['priority']


