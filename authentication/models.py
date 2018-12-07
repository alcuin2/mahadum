from passlib.hash import pbkdf2_sha256
from django.db import models
from django_extensions.db.fields import RandomCharField

from courses.models import Course


class Parent(models.Model):

    id = RandomCharField(unique=True, include_alpha=False,
                         length=12, primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200, editable=False)
    first_name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return "Parent: {0} {1}".format(self.first_name, self.surname)


class School(models.Model):

    id = RandomCharField(unique=True, include_alpha=False,
                         length=12, primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=200, editable=False)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return "School: {0}".format(self.name)


class Teacher(models.Model):

    id = RandomCharField(unique=True, include_alpha=False,
                         length=12, primary_key=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return "Teacher: {0} {1}".format(self.first_name, self.surname)
