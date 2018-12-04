import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from courses.models import Course, Lesson
from main.models import Kid, RegisteredCourse, Tracker


@csrf_exempt
def register_course(request):
    if request.method == "POST":
        body = json.loads(request.body)
        try:
            course = Course.objects.get(id=body['course_id'])
            kid = Kid.objects.get(id=body['kid_id'])
            if len(RegisteredCourse.objects.filter(
                    kid=kid, course=course)) == 0:
                new_course = RegisteredCourse(course=course, kid=kid)
                new_course.save()
                return JsonResponse({"statusMsg": "Course registered for kid"}, status=200)
            else:
                return JsonResponse({"statusMsg": "Course already registered for kid."}, status=400)
        except:
            return JsonResponse({"statusMsg": "Failed, check ids."}, status=400)
    else:
        return JsonResponse({"statusMsg": "Please, use POST method"}, status=400)


@csrf_exempt
def start_lesson(request):
    if request.method == "POST":
        body = json.loads(request.body)
        try:
            lesson = Lesson.objects.get(id=body['lesson_id'])
            kid = Kid.objects.get(id=body['kid_id'])
            if len(RegisteredCourse.objects.filter(
                    kid=kid, course=lesson.course)) == 0:
                return JsonResponse({"statusMsg": "First register kid for this course"}, status=400)
            else:
                reg_course = RegisteredCourse.objects.get(
                    kid=kid, course=lesson.course)
                new_tracker = Tracker(
                    lesson=lesson
                )
                new_tracker.save()
                reg_course.tracker = new_tracker
                reg_course.save()

        except:
            return JsonResponse({"statusMsg": "Failed, check ids."}, status=400)
