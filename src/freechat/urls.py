
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('adminsql/', admin.site.urls),
    path('chat/',include('chat.urls')),
]
