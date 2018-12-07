from django.contrib import admin
from authentication.models import Parent, School, Teacher
from main.models import Kid


def number_of_kids(obj):
    if isinstance(obj, Parent):
        return Kid.objects.filter(parent=obj).count()
    if isinstance(obj, School):
        return Kid.objects.filter(school=obj).count()


class ParentAdmin(admin.ModelAdmin):

    list_display = (
        "first_name",
        "surname",
        "email",
        "mobile",
        number_of_kids
    )

    search_fields = (
        "first_name",
        "surname",
        "email",
        "mobile"
    )


class SchoolAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "address",
        "id",
        "email",
        "mobile",
        number_of_kids
    )

    search_fields = (
        "name",
        "address",
        "email",
        "mobile"
    )


admin.site.register(Parent, ParentAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Teacher)
