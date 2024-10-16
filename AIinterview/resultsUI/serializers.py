from rest_framework import serializers
from .models import interviewTest

class fileSerializers(serializers.ModelSerializer):
    # file = serializers.FileField()
    class Meta:
        model = interviewTest
        fields = ('file',)