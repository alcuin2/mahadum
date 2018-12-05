from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from courses.models import Course, Lesson


def get_all_courses(request):

    if request.method == "GET":
        courses = Course.objects.all()
        list_of_courses = []
        for course in courses:
            data = {}
            data['id'] = course.id
            data['title'] = course.title
            data['short_description'] = course.short_description
            data['owner'] = course.owner.name
            data['introductory_video'] = course.introductory_video
            list_of_courses.append(data)
        return JsonResponse({"statusMsg": "All Courses", "courses": list_of_courses}, status=200)
    else:
        return JsonResponse({"statusMsg": "Please, use GET method"}, status=400)


@csrf_exempt
def get_course_details(request):

    if request.method == "POST":
        body = json.loads(request.body)
        try:
            course = Course.objects.get(id=body["course_id"])
            lessons = Lesson.objects.filter(
                course=course).order_by("lesson_number")
            list_of_lessons = []
            for lesson in lessons:
                data = {}
                data['id'] = lesson.id
                data['title'] = lesson.title
                data['body'] = lesson.body
                data['video_link'] = lesson.video_link
                data['lesson_number'] = lesson.lesson_number
                list_of_lessons.append(data)
            return JsonResponse({"statusMsg": "Course details", "id": course.id, "title": course.title,
                                 "short_description": course.short_description, "owner": course.owner.name, "introductory_video": course.introductory_video,
                                 "lessons": list_of_lessons}, status=200)
        except:
            return JsonResponse({"statusMsg": "Course is not found"}, status=400)
    else:
        return JsonResponse({"statusmsg": "Please, use POST method"}, status=400)
