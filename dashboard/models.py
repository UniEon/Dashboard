from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.core.urlresolvers import reverse
from autoslug import AutoSlugField
from django.conf import settings
# Create your models here.


#models for questions
class Question(models.Model):
    title=models.CharField(max_length=250)
    slug=AutoSlugField(populate_from='title', unique_with='created')
    author=models.ForeignKey(User, related_name='asked_questions')
    body=models.TextField(max_length=2000)
    created=models.DateTimeField(default=timezone.now)
    updated=models.DateTimeField(auto_now=True)
    tags = TaggableManager()
    family='Question'

    class Meta:
        ordering= ('-created',)
        
    def get_absolute_url(self):
        return reverse('question_detail',
                       args=[self.created.year,
                             self.created.strftime('%m'),
                             self.created.strftime('%d'),
                             self.slug])
    
    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers')
    name=models.ForeignKey(User, related_name='given_answers')
    body=models.TextField(max_length=2000)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
    def __str__(self):
        return 'Answer by {} on {}'.format(self.name, self.question)
    

#Story models

class Story(models.Model):
    title=models.CharField(max_length=250)
    slug=AutoSlugField(populate_from='title', unique_with='created')
    author=models.ForeignKey(User, related_name='posted_stories')
    source = models.URLField(max_length=250)
    created= models.DateTimeField(default=timezone.now)
    updated=models.DateTimeField(auto_now=True)
    tags = TaggableManager()
    family='News'

    class Meta:
        ordering=('-created',)
    def get_absolute_url(self):
        return reverse('story_detail',
                       args=[self.created.year,
                             self.created.strftime('%m'),
                             self.created.strftime('%d'),
                             self.slug])
    def __str__(self):
        return self.title

class Comment(models.Model):
    story=models.ForeignKey(Story, related_name='comments',default='')
    name= models.ForeignKey(User, related_name='story_comments')
    body = models.TextField(max_length=2000)
    created = models.DateTimeField(auto_now_add = True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.story)
    
#profile

class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth=models.DateField(blank=True, null=True)
    work_or_study=models.CharField(max_length=100, blank=True, null=True)
    skills=models.CharField(max_length=500, blank=True, null=True)
    
    
    def __str__(self):
        if self.user.first_name:
            screen_name=self.user.get_full_name()
            return '{}'.format(screen_name)
        else:
            screen_name=self.user.get_username()
            return '{}'.format(screen_name)
#        return 'Profile for user {}'.format(self.user.username)


#feedback
class Feedback(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=50)
    feedback=models.TextField(max_length=1500)
    created=models.DateTimeField(auto_now_add=True)
    

class q_notify(models.Model):
    Actor=models.ForeignKey(User, related_name='q_activities')
    Object=models.ForeignKey(Question, related_name='q_notif')
    Target=models.ForeignKey(User, related_name='q_events')
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '{} answered your question {}.'.format\
               (self.Actor.profile, self.Object)
class s_notify(models.Model):
    Actor=models.ForeignKey(User, related_name='s_activities')
    Object=models.ForeignKey(Story, related_name='s_notif')
    Target=models.ForeignKey(User, related_name='s_events')
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '{} commented on your news {}.'.format\
               (self.Actor.profile, self.Object)
    

    
