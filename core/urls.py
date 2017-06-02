from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'', include('crawler.urls', namespace='crawler-api')),
    url(r'^admin/', include(admin.site.urls)),
]
