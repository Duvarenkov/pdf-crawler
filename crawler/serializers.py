# Third Party
from rest_framework import serializers

# App
from .models import DocumentModel, URLModel


class DocumentSerializer(serializers.ModelSerializer):
    urls_count = serializers.SerializerMethodField()

    def get_urls_count(self, obj):
        return obj.urlmodel_set.count()

    class Meta:
        model = DocumentModel
        fields = (
            'name', 'urls_count', 'uuid', 'urls'
        )


class URLSerializer(serializers.ModelSerializer):
    documents_count = serializers.SerializerMethodField()

    def get_documents_count(self, obj):
        return obj.documents.count()

    class Meta:
        model = URLModel
        fields = (
            'uuid', 'url', 'is_alive', 'documents_count'
        )
