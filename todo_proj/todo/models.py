from django.db import models

TASK_DONE = True
TASK_TODO = False
TASK_STATUS = (
        (TASK_DONE, 'Done'),
        (TASK_TODO, 'Not done'),
    )

TASK_HIGH_PRIORITY = 0
TASK_MIDDLE_PRIORITY = 1
TASK_LOW_PRIORITY = 2
TASK_PRIORITY = (
    (TASK_HIGH_PRIORITY, 'red'),
    (TASK_MIDDLE_PRIORITY, 'orange'),
    (TASK_LOW_PRIORITY, 'white'),
)


class Project(models.Model):
    color = models.CharField(max_length=20, default='red')
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='projects')
    project_name = models.CharField(max_length=100)

    def __str__(self):
        return self.project_name


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    task = models.CharField(max_length=300)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=TASK_STATUS)
    priority = models.CharField(max_length=10, choices=TASK_PRIORITY)

    class Meta:
        ordering = ['priority']


