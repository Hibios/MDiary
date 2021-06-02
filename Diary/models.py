from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from transliterate import translit

from taggit.managers import TaggableManager


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='media/', blank=True, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    instance.profile.save()


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter()


class Event(models.Model):
    event_title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=250, unique_for_date='pub_date', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_posts')
    event_description = models.CharField(max_length=1000)
    pub_date = models.DateField('date published', default=timezone.now)
    event_photo = models.ImageField(upload_to='media/', blank=True, null=True)
    tags = TaggableManager()

    class Meta:
        ordering = ('-pub_date',)

    def get_absolute_url(self):
        return reverse('Diary:event_detail',
                       args=[self.pub_date.year,
                             self.pub_date.month,
                             self.pub_date.day,
                             self.slug])

    def get_edit_url(self):
        return reverse('Diary:edit_event',
                       args=[self.pub_date.year,
                             self.pub_date.month,
                             self.pub_date.day,
                             self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(str(self.event_title), 'ru', reversed=True))
        return super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.event_title

    objects = models.Manager()
    published = PublishedManager()
