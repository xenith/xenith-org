"""
Model classes and methods for the blog app
"""

from django.db import models
from django.conf import settings
from datetime import datetime
from taggit.managers import TaggableManager


class Blog(models.Model):
    """
    A single blog that consists of multiple articles
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField("blog title", max_length=100)
    tagline = models.CharField("blog tagline", max_length=200)
    description = models.TextField("blog description")
    posts_per_page = models.PositiveIntegerField(default=10)

    def __unicode__(self):
        return self.title


class Article(models.Model):
    """
    A single article
    """
    blog = models.ForeignKey(Blog)
    title = models.CharField("article title", max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    published_date = models.DateTimeField(
        default=datetime.now,
        help_text="The date and time this article shall appear online.")
    expiration_date = models.DateTimeField(
        blank=True, null=True,
        help_text="Leave blank if the article does not expire.")
    created_time = models.DateTimeField(auto_now_add=True, editable=False)
    edited_time = models.DateTimeField(auto_now=True, editable=False)
    series = models.CharField("Series name", max_length=255,
                              blank=True, default="")
    slug = models.SlugField("article slug", unique_for_year=published_date)
    teaser = models.TextField("article teaser")
    content = models.TextField("article content")
    markup_type = models.CharField(max_length=10, choices=(
        ("html", "HTML"),
        ("rst", "reStructuredText"),
        ("markdown", "Markdown"),
    ), default="markdown")
    published = models.BooleanField("published?", default=False)
    allow_comments = models.BooleanField("allow comments?", default=True)
    show_comments = models.BooleanField("show comments?", default=True)

    objects = models.Manager()
    tags = TaggableManager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["-published_date"]
        get_latest_by = "published_date"


class Attachment(models.Model):
    """
    An uploaded file attached to an article
    """
    path = models.FileField(upload_to=lambda inst, fn:
                            'attachment/%s/%s/%s' % (datetime.now().year, inst.article.slug, fn))
    article = models.ForeignKey(Article)

    def __unicode__(self):
        return self.path


class Microblog(models.Model):
    """
    A ticker-style widget for displaying data from a microblog service,
    such as Twitter.
    """
    enabled = models.BooleanField("enabled?", default=True)
    blog = models.ForeignKey(Blog)
    service = models.CharField("service", max_length=100,
                               default="twitter", blank=True)
    url = models.CharField("url", max_length=255, default="", blank=True)
    username = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)
    poll_minutes = models.IntegerField(default=10)
    template_path = models.CharField(max_length=255)
    next_poll_time = models.DateTimeField("time to next poll",
                                          auto_now_add=True)

    objects = models.Manager()
    tags = TaggableManager()
