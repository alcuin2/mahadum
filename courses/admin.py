from django.contrib import admin

from courses.models import CourseOwner, Course, Lesson
from main.models import RegisteredCourse


def number_of_kids(obj):
    return RegisteredCourse.objects.filter(course=obj).count()


def courses(obj):
    courses = ""
    for course in Course.objects.filter(owner=obj):
        courses + " " + course.title
    return courses


class CourseAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "id",
        "owner",
        "short_description",
        "linked_intro_video",
        number_of_kids
    )

    search_fields = (
        "title",
    )


class LessonAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "course",
        "linked_intro_video",
        "linked_body_pdf",
        "lesson_number"
    )

    search_fields = (
        "title",
        "course",
    )


class CourseOwnerAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "mobile",
        courses
    )

    search_fields = (
        "name",
        "email"
    )


admin.site.register(CourseOwner, CourseOwnerAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
