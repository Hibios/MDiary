from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages

from .forms import ProfileForm, UserForm, ProfileImageForm, EventForm, EventPhotoForm, SearchForm
from .models import Event
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .functions import do_pagination


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect('Diary:profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileImageForm()
    return render(request, 'Diary/edit_profile.html', {
        'user_form': user_form,
        'image_form': profile_form,
    })


@login_required
def update_event(request, year, month, day, event):
    event = get_object_or_404(Event, slug=event, pub_date__year=year, pub_date__month=month, pub_date__day=day)
    if request.method == 'POST':
        event_form = EventForm(request.POST, instance=event)
        event_image_form = EventPhotoForm(request.POST, request.FILES, instance=event)
        if event_form.is_valid():
            event_image_form.save()
            event_form.save()
            return redirect('Diary:events')
    else:
        event_form = EventForm(instance=event)
        event_image_form = EventPhotoForm()
    return render(request, 'Diary/edit_event.html', {'event': event, 'event_form': event_form,
                                                     'event_image_form': event_image_form, })


@login_required
def add_event(request):
    if request.method == "POST":
        event_form = EventForm(request.POST, request.FILES)
        if event_form.is_valid():
            event_form.save()
            events = Event.published.all()
            paginator = Paginator(events, 3)
            return HttpResponseRedirect(f'/events?page={paginator.num_pages}')
    else:
        event_form = EventForm()
    return render(request,
                  'Diary/edit_event.html',
                  context={'event_form': event_form, })


def register_request(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("Diary:profile")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = ProfileForm()
    return render(request,
                  'Diary/register.html',
                  context={"register_form": form})


@login_required(login_url='Diary:login')
def index(request):
    return render(
        request,
        'Diary/profile.html')


@login_required(login_url='Diary:login')
def show_events(request):
    events = Event.published.all()
    events, page = do_pagination(events, 3, request)
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            events = Event.objects.filter(event_title__icontains=search_form.cleaned_data['search_text'])
            events, page = do_pagination(events, 3, request)
            return render(request,
                          'Diary/events.html',
                          {'page': page,
                           'events': events,
                           'search_form': search_form})
    else:
        search_form = SearchForm()
    return render(request,
                  'Diary/events.html',
                  {'page': page,
                   'events': events,
                   'search_form': search_form})


def event_detail(request, year, month, day, event):
    event = get_object_or_404(Event, slug=event, pub_date__year=year, pub_date__month=month, pub_date__day=day)
    return render(request, 'Diary/event.html', {'event': event})
