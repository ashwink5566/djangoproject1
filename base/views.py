from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, User, Messages
from .forms import RoomForm, UserForm


def loginpage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User not found')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User not exist')

    context = {'page':page}
    return render(request, 'base/login_reg.html', context)


def logoutuser(request):

    logout(request)
    return redirect('home')


def registeruser(request):

    forms = UserCreationForm

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'an error occured')


    context = {'forms':forms}
    return render(request,'base/login_reg.html', context)

def home(request):

    query = request.GET.get('q') if request.GET.get('q') != None else ''
    
    topics = Topic.objects.all()
    room_message= Messages.objects.filter(
        Q(room__topic__name__icontains=query)
    )
    rooms = Room.objects.filter(
        Q(topic__name__icontains=query) |
        Q(name__icontains=query) |
        Q(description__icontains=query)
        )
    
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count':room_count, 'room_message':room_message}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    messages1 = room.messages_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Messages.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'messages1':messages1,
               'participants': participants}
    return render(request, 'base/room.html', context)

def profile(request, pk):
    user = User.objects.get(id=pk)
    room_message = user.messages_set.all()
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 'room_message':room_message, 'topics':topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):

    forms = RoomForm
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    

    context = {'forms': forms, 'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    
    room = Room.objects.get(id=pk)
    forms = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('you are not allowed')
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = request.POST.get('topic')
        room.description = request.POST.get('description')
        return redirect('home')

    context = {'forms': forms, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    
    if request.user != room.host:
        return HttpResponse('you are not allowed')
    

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessages(request, pk):
    message = Messages.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('you are not allowed')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    context = {'form':form}
    return render(request, 'base/update-user.html', context)


def topic(request):

    query = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(
        Q(name__icontains=query)
    )

    context = {'topics':topics}
    return render(request,'base/topics.html', context)

def activity(request):

    room_message= Messages.objects.all()

    context = {'room_message':room_message}
    return render(request, 'base/activity.html', context)