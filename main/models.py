from django.db import models
from django_extensions.db.fields import RandomCharField

from authentication.models import Parent, School
from courses.models import Course, Lesson

# Create your models here.


class Kid(models.Model):

    id = RandomCharField(unique=True, include_alpha=False,
                         length=12, primary_key=True)
    name = models.CharField(max_length=200, help_text="Full name of kid")
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "Kid: {0}".format(self.name)


class Tracker(models.Model):

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return self.lesson


class RegisteredCourse(models.Model):

    kid = models.ForeignKey(Kid, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tracker = models.ForeignKey(
        Tracker, on_delete=models.CASCADE, null=True, editable=False)

    def __str__(self):
        return self.kid
