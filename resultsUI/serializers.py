from rest_framework import serializers
from .models import LinkEntry , BatchEntry

class LinkSerializer(serializers.Serializer):
    links = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(),
            
        ),
        allow_empty=False,
    )

class LinkEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkEntry
        fields = ['link', 'unique_id', 'batch_id', 'status', 'video_path']
        read_only_fields = ['unique_id', 'batch_id', 'status', 'video_path']

class BatchEntrySerializer(serializers.ModelSerializer):
    links = LinkEntrySerializer(many=True, read_only=True)

    class Meta:
        model = BatchEntry
        fields = ['batch_id', 'status', 'created_at', 'links']
        read_only_fields = ['batch_id', 'status', 'created_at', 'links']

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchEntry
        fields = ['batch_id', 'results']