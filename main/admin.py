from django.contrib import admin
from main.models import Kid, RegisteredCourse, Book
from authentication.models import Parent
from django.utils.html import format_html


def number_of_courses(obj):
    return RegisteredCourse.objects.filter(kid=obj).count()


def parent_name(obj):
    parent = Parent.objects.get(email=obj.parent.email)
    return "{0} {1}".format(parent.first_name, parent.surname)


def parent_email(obj):
    parent = Parent.objects.get(email=obj.parent.email)
    return "{0}".format(parent.email)


class KidAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        parent_name,
        parent_email,
        "school",
        number_of_courses
    )
    empty_value_display = '-- empty --'

    search_fields = (
        "name",
    )


class RegisteredCourseAdmin(admin.ModelAdmin):

    list_display = (
        "kid",
        "course"
    )

    list_filter = (
        "course",
    )


class BookAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "author",
        "price",
        "cover_link"
    )


admin.site.register(Kid, KidAdmin)
admin.site.register(RegisteredCourse, RegisteredCourseAdmin)
admin.site.register(Book, BookAdmin)
