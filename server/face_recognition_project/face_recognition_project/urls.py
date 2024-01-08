"""
URL configuration for face_recognition_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from face_recognition_app.views import face_recognition,add_user_with_embedding,get_users_with_logs,add_user,verify_access
urlpatterns = [
    path('admin/', admin.site.urls),
    path('face_recognition/', face_recognition, name='face_recognition'),
    path('add_user_with_embedding/', add_user_with_embedding, name='add_user_with_embedding'),
    path('get_users_with_logs/', get_users_with_logs, name='get_users_with_logs'),
    path('add_user/', add_user, name='add_user'),
     path('verify_access/', verify_access, name='verify_access'),
    #add_user
]
