"""mahadum_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from authentication.views import *
from main.views import register_course

admin.site.site_header = "Mahadum Admin"

urlpatterns = [
    url(r'^api/parent/create$', create_parent),
    url(r'^api/parent/login$', login_parent),
    url(r'^api/parent/add/kid', add_kid),
    url(r'^api/parent/course/registerkid', register_course),
    url(r'^api/parent/password/change', change_parent_password),
    url(r'^api/parent/password/validate', validate_parent_password),
    url(r'^admin/', admin.site.urls)
]
