import json
from passlib.hash import pbkdf2_sha256
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from authentication.models import Parent, Teacher, School
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError

from main.models import Kid, RegisteredCourse
from courses.models import Course

# Create your views here.


@csrf_exempt
def create_parent(request):

    if request.method == "POST":
        body = json.loads(request.body)
        try:
            parent = Parent(
                email=body['email'],
                first_name=body['first_name'],
                surname=body['surname'],
                mobile=body['mobile']
            )
            parent.password = pbkdf2_sha256.hash(body['password'])
            parent.save()
            return JsonResponse({"statusMsg": "New Parent created", "id": parent.id, "Email": parent.email, "first_name": parent.first_name,
                                 "surname": parent.surname, "mobile": parent.mobile})
        except IntegrityError:
            return JsonResponse({"statusMsg": "Email already exists"}, status=400)

    else:
        return JsonResponse({"statusMsg": "Please, use POST method"}, status=400)


@csrf_exempt
def login_parent(request):

    if request.method == "POST":
        body = json.loads(request.body)

        try:
            parent = Parent.objects.get(email=body['email'])
            password = body['password']

            if pbkdf2_sha256.verify(password, parent.password):
                kids = Kid.objects.filter(parent=parent)
                kids_details = []
                if len(kids) > 0:
                    for kid in kids:
                        registered_courses = RegisteredCourse.objects.filter(
                            kid=kid)
                        data = {}
                        data['name'] = kid.name
                        data['id'] = kid.id
                        data['number_of_courses'] = len(registered_courses)
                        list_of_courses = []
                        if len(registered_courses) > 0:
                            for course in registered_courses:
                                course_obj = Course.objects.get(
                                    id=course.course.id)
                                course_data = {}
                                course_data['id'] = course_obj.id
                                course_data['title'] = course_obj.title
                                list_of_courses.append(course_data)
                                data["courses"] = list_of_courses
                        else:
                            data["courses"] = []

                        kids_details.append(data)
                return JsonResponse({"statusMsg": "Parent Logged in", "id": parent.id,
                                     "first_name": parent.first_name, "surname": parent.surname,
                                     "email": parent.email, "mobile": parent.mobile,
                                     "number_of_kids": len(kids), "kids": kids_details}, status=200)
            else:
                return JsonResponse({"statusMsg": "Login Failed"}, status=400)
        except:
            return JsonResponse({"statusMsg": "Login Failed"}, status=400)
    else:
        return JsonResponse({"statusMsg": "Please, use POST method"}, status=400)


@csrf_exempt
def add_kid(request):

    if request.method == "POST":
        body = json.loads(request.body)

        try:
            parent = Parent.objects.get(id=body["parent_id"])
            kid = Kid(
                name=body['full_name'],
                parent=parent
            )
            kid.save()
            return JsonResponse({"statusMsg": "Kid added successfull",
                                 "id": kid.id,
                                 "fullname": kid.name
                                 }, status=200)

        except:
            return JsonResponse({"statusMsg": "Parent not found"}, status=400)
    else:
        return JsonResponse({"statusMsg": "Please, use POST method"}, status=400)


@csrf_exempt
def change_parent_password(request):

    if request.method == "POST":
        body = json.loads(request.body)
        try:
            parent = Parent.objects.get(id=body["parent_id"])
            parent.password = pbkdf2_sha256.hash(body['password'])
            parent.save()
            return JsonResponse({"statusMsg": "Password changed",
                                 "type": "Parent",
                                 "id": parent.id,
                                 }, status=200)

        except:
            return JsonResponse({"statusMsg": "Parent not found"}, status=400)

    else:
        return JsonResponse({"statusMsg": "Please, use POST method"}, status=400)


@csrf_exempt
def validate_parent_password(request):

    if request.method == "POST":
        body = json.loads(request.body)

        try:
            parent = Parent.objects.get(id=body["parent_id"])
            flag = pbkdf2_sha256.verify(body['password'], parent.password)
            if flag:
                return JsonResponse({"statusMsg": "Password validated"}, status=200)
            else:
                return JsonResponse({"statusMsg": "Invalid password"}, status=400)

        except:
            return JsonResponse({"statusMsg": "Parent not found"}, status=400)

    else:
        return JsonResponse({"statusMsg": "Please, use POST method"}, status=400)


@csrf_exempt
def create_teacher(request):

    if request.method == "POST":
        body = json.loads(request.body)
        try:
            school = School.objects.get(id=body["school_id"])
            teacher = Teacher(
                email=body['email'],
                first_name=body['first_name'],
                surname=body['surname'],
                mobile=body['mobile'],
                school=school
            )
            teacher.password = pbkdf2_sha256.hash(body['password'])
            teacher.save()
            return JsonResponse({"statusMsg": "New Teacher created", "id": teacher.id, "Email": teacher.email, "first_name": teacher.first_name,
                                 "surname": teacher.surname, "mobile": teacher.mobile})
        except IntegrityError:
            return JsonResponse({"statusMsg": "Email already exists"}, status=400)

    else:
        return JsonResponse({"statusMsg": "Please, use POST method"}, status=400)


@csrf_exempt
def teacher_login(request):

    if request.method == "POST":
        body = json.loads(request.body)

        try:
            teacher = Teacher.objects.get(email=body['email'])
            password = body['password']

            if pbkdf2_sha256.verify(password, teacher.password):
                courses = RegisteredCourse.objects.filter(
                    course=teacher.course, school=teacher.school)
                list_of_kids = []
                for course in courses:
                    data = {}
                    data["name"] = course.kid.name
                    data["parent"] = course.kid.parent.first_name + \
                        " " + course.kid.parent.surname
                    data["course"] = course.course.title
                    list_of_kids.append(data)
                return JsonResponse({"statusMsg": "Teacher Login", "Kids": list_of_kids}, status=200)

            else:
                return JsonResponse({"statusMsg": "Login Failed"}, status=400)

        except:
            return JsonResponse({"statusMsg": "Login Failed"}, status=400)
    else:
        return JsonResponse({"statusMsg": "Please, use POST method"}, status=400)
