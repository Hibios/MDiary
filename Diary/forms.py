from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Profile, Event


class ProfileForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Почта')
    first_name = forms.CharField(required=True, label='Имя')
    last_name = forms.CharField(required=True, label='Фамилия')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for _object in self.fields.values():
            _object.widget = forms.TextInput(attrs={'placeholder': _object.label, 'class': 'form-control shadow-none'})

    # Переопределяем подкласс Meta, перезаписывая кортеж fields с добавлением поля email
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2",)

    # Переопределяем метод save, определяя новому пользователю значение атрибута email
    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control shadow-none', 'placeholder': 'Никнейм',
                                                     'value': '{{ user.get_username }}', 'type': 'text'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control shadow-none', 'placeholder': 'Имя',
                                                       'value': '{{ user.first_name }}', 'type': 'text'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control shadow-none', 'placeholder': 'Фамилия',
                                                      'value': '{{ user.last_name }}', 'type': 'text'})
        self.fields['email'].widget.attrs.update({'class': 'form-control shadow-none',
                                                  'placeholder': 'Электронная почта', 'value': '{{ user.email }}',
                                                  'type': 'text'})


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('event_title', 'event_description', 'author', 'tags', 'event_photo', )

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['event_title'].widget.attrs.update({'class': 'form-control shadow-none', 'placeholder': 'Заголовок',
                                                        'value': '{{ event }}', 'type': 'text'})
        self.fields['event_description'].widget.attrs.update({'class': 'form-control shadow-none',
                                                              'placeholder': 'Описание',
                                                              'value': '{{ event.event_description }}', 'type': 'text'})
        self.fields['author'].widget.attrs.update({'class': 'form-control shadow-none', 'placeholder': 'Автор',
                                                   'value': '{{ event.author }}', 'type': 'text'})
        self.fields['tags'].widget.attrs.update({'class': 'form-control shadow-none', 'placeholder': 'Теги',
                                                 'value': '{{ event.tags.all|join:", " }}', 'type': 'text'})
        self.fields['event_photo'].widget.attrs.update(
            {'style': 'opacity: 0.0; position: relative; width: 100%; height:100%; '})


class EventPhotoForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('event_photo', )

    def __init__(self, *args, **kwargs):
        super(EventPhotoForm, self).__init__(*args, **kwargs)

        self.fields['event_photo'].widget.attrs.update(
            {'style': 'opacity: 0.0; position: relative; width: 100%; height:100%; '})


class ProfileImageForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('profile_photo', )

    def __init__(self, *args, **kwargs):
        super(ProfileImageForm, self).__init__(*args, **kwargs)

        self.fields['profile_photo'].widget.attrs.update(
            {'style': 'opacity: 0.0; position: relative; width: 100%; height:100%; '})


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none', 'placeholder': 'Логин', 'type': 'text'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control shadow-none', 'placeholder': 'Пароль', 'type': 'password'}))


class PasswordResetUserForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control shadow-none', 'placeholder': 'Почта', 'type': 'text'})


class SetPasswordUserForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordUserForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control shadow-none', 'placeholder': 'Пароль', 'type': 'password'})
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control shadow-none', 'placeholder': 'Повторите пароль', 'type': 'password'})


class SearchForm(forms.Form):
    search_text = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none', 'placeholder': 'Найти событие',
               'type': 'text', 'aria-describedby': 'basic-addon1'}))
