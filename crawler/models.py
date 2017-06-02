from __future__ import unicode_literals

import uuid

from django.db import models
from urllib.request import urlopen, URLError


class DocumentModel(models.Model):
    """
    Model representing document.
    """

    name = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def urls(self):
        """
        Returns a list of urls in a document. Each url is a string.
        """
        return [url_obj.url for url_obj in self.urlmodel_set.all()]

    def __unicode__(self):
        return '%s - %s' % (self.name, self.created_at)


class URLModel(models.Model):
    """
    Model representing URL.
    """

    url = models.CharField(max_length=2000)
    uuid = models.UUIDField(default=uuid.uuid4)
    documents = models.ManyToManyField(DocumentModel)

    def is_alive(self):
        """
        Checks if url is alive.

        Returns True for answers 1XX, 2XX, 3XX.
        Returns False otherwise.
        """
        try:
            resp = urlopen(self.url)
            if resp.code < 400:
                return True
        except URLError:
            pass

        return False

    def __unicode__(self):
        return self.url
