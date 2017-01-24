from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    is_active = models.SmallIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField()

    def __unicode__(self):
        return '%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('view_blog_category', None, {'slug':self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    is_active = models.SmallIntegerField(default=1)
    is_spam = models.SmallIntegerField(default=0)
    category = models.ForeignKey(Category)
    author = models.ForeignKey(User)

    def __unicode__(self):
        return '%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('view_blog_post', None, { 'slug': self.slug })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post, related_name = "user_posts")
    user = models.ForeignKey(User, related_name = "post_user")
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text

class Likes(models.Model):
    post = models.ForeignKey(Post, related_name = "like_post")
    user = models.ForeignKey(User, related_name = "like_user")
    created_on = models.DateTimeField(auto_now_add=True)

class PostImage(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    post = models.ForeignKey(Post, related_name = "post_image")
    user = models.ForeignKey(User, related_name = "user_image")
    created_on = models.DateTimeField(auto_now_add=True)
