import jwt
from mahadum_django.settings import SECRET_KEY
from django.http import HttpResponseBadRequest


class AuthSecure(object):

    def process_request(self, request):
        try:
            print("I'm here!!!!")
            token = request.META.get('MAHADUM-TOKEN')
            decoded = jwt.decode(token, SECRET_KEY)
            request.email = decoded['email']
            request.type = decoded['type']
            request.id = decoded['id']
            return None
        except:
            return HttpResponseBadRequest

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
