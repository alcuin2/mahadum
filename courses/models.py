from passlib.hash import pbkdf2_sha256
from django.db import models
from django_extensions.db.fields import RandomCharField
from django.utils.html import format_html
from django.core.exceptions import ValidationError


class CourseOwner(models.Model):

    id = RandomCharField(unique=True, include_alpha=False,
                         length=12, primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200, editable=False)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return "CourseOwner: {0}".format(self.name)


class Course(models.Model):
    id = RandomCharField(unique=True, include_alpha=False,
                         length=12, primary_key=True)
    owner = models.ForeignKey(CourseOwner, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=300)
    long_description = models.TextField()
    introductory_video = models.URLField(
        help_text="Youtube link to the course intro")

    def linked_intro_video(self):
        return format_html(
            '<a href="{}" target="_blank ">{}</a>',
            self.introductory_video,
            self.introductory_video,
        )

    def __str__(self):
        return "Course: {0}".format(self.title)


class Lesson(models.Model):
    id = RandomCharField(unique=True, include_alpha=False,
                         length=12, primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.URLField(help_text="Link to pdf content")
    video_link = models.URLField(help_text="Youtube link to the lesson")
    lesson_number = models.IntegerField(
        help_text="Serial number of Lesson in course, must be unique.")

    def linked_intro_video(self):
        return format_html(
            '<a href="{}" target="_blank ">{}</a>',
            self.video_link,
            self.video_link
        )

    def linked_body_pdf(self):
        return format_html(
            '<a href="{}" target="_blank ">{}</a>',
            self.body,
            self.body
        )

    def clean(self):
        if Lesson.objects.filter(course=self.course, lesson_number=self.lesson_number).count() > 0:
            raise ValidationError(
                "Lesson number already exists for this course.")

    def __str__(self):
        return "Lesson: {0}".format(self.title)
