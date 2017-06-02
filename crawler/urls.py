from django.conf.urls import url, include
from rest_framework import routers
from .views import DocumentViewSet, URLViewSet, FileUploadView

router = routers.DefaultRouter()
router.register(r'documents', DocumentViewSet)
router.register(r'urls', URLViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view())
]
