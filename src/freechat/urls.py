
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('adminsqlite/', admin.site.urls),
    path('chat/',include('chat.urls')),
]
