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
        return ('view_blog_categoty', None, {'slug':self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField()
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
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text


# BEGIN;
# --
# -- Create model Category
# --
# CREATE TABLE `blogs_category` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `title` varchar(100) NOT NULL UNIQUE, `slug` varchar(100) NOT NULL UNIQUE, `is_active` smallint NOT NULL, `created_on` datetime(6) NOT NULL, `updated_on` datetime(6) NOT NULL);
# --
# -- Create model Comment
# --
# CREATE TABLE `blogs_comment` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `text` longtext NOT NULL, `created_on` datetime(6) NOT NULL);
# --
# -- Create model Post
# --
# CREATE TABLE `blogs_post` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `title` varchar(200) NOT NULL UNIQUE, `slug` varchar(200) NOT NULL UNIQUE, `body` longtext NOT NULL, `created_on` datetime(6) NOT NULL, `updated_on` datetime(6) NOT NULL, `is_active` smallint NOT NULL, `is_spam` smallint NOT NULL, `author_id` integer NOT NULL, `category_id` integer NOT NULL);
# --
# -- Add field post to comment
# --
# ALTER TABLE `blogs_comment` ADD COLUMN `post_id` integer NOT NULL;
# ALTER TABLE `blogs_comment` ALTER COLUMN `post_id` DROP DEFAULT;
# --
# -- Add field user to comment
# --
# ALTER TABLE `blogs_comment` ADD COLUMN `user_id` integer NOT NULL;
# ALTER TABLE `blogs_comment` ALTER COLUMN `user_id` DROP DEFAULT;
# ALTER TABLE `blogs_post` ADD CONSTRAINT `blogs_post_author_id_c7d05c07_fk_auth_user_id` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`);
# ALTER TABLE `blogs_post` ADD CONSTRAINT `blogs_post_category_id_10b67abe_fk_blogs_category_id` FOREIGN KEY (`category_id`) REFERENCES `blogs_category` (`id`);
# ALTER TABLE `blogs_comment` ADD CONSTRAINT `blogs_comment_post_id_670c072f_fk_blogs_post_id` FOREIGN KEY (`post_id`) REFERENCES `blogs_post` (`id`);
# ALTER TABLE `blogs_comment` ADD CONSTRAINT `blogs_comment_user_id_e0b0b977_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
# COMMIT;
