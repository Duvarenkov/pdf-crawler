from rest_framework import viewsets, mixins
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DocumentModel, URLModel
from .serializers import DocumentSerializer, URLSerializer
from .utils import get_links_from_pdf


class DocumentViewSet(viewsets.GenericViewSet):
    """
    API endpoint that allows documents to be viewed.
    """

    queryset = DocumentModel.objects.all()
    serializer_class = DocumentSerializer
    lookup_field = 'uuid'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        resp_dict = [
            {'uuid': doc['uuid'],
             'name': doc['name'],
             'urls_count': doc['urls_count']} for doc in serializer.data
        ]

        return Response(resp_dict)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data['urls'])


class URLViewSet(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """
    API endpoint that allows urls to be viewed.
    """

    queryset = URLModel.objects.all()
    serializer_class = URLSerializer
    lookup_field = 'uuid'


class FileUploadView(APIView):
    """
    API endpoint that allows pdf documents to be uploaded.
    """

    parser_classes = (FileUploadParser,)

    def post(self, request, filename):
        file_obj = request.data['file']
        links = get_links_from_pdf(file_obj)

        document = DocumentModel.objects.create(name=filename)
        for link in links:
            try:
                url_obj = URLModel.objects.get(url=link)
            except URLModel.DoesNotExist:
                url_obj = URLModel.objects.create(url=link)

            url_obj.documents.add(document)

        serializer = DocumentSerializer(document)

        return Response(serializer.data)
