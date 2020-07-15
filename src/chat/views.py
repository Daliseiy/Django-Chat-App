from django.shortcuts import render
from random_username.generate import generate_username

# Create your views here.
def index(request):
    return render(request, 'index.html',{})

def room(request, room_name):
    user = generate_username(1)[0]
    author = user
    return render(request, 'room.html', {
        'room_name': room_name,
        'username':user,
        'author':author
    })

def b(request):
    return render(request, 'b.html',{})