from rest_framework import serializers

from georepo.models import Dataset


class DatasetSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    identifier = serializers.SerializerMethodField()
    last_update = serializers.SerializerMethodField()

    class Meta:
        model = Dataset
        fields = [
            'name',
            'identifier',
            'last_update'
        ]

    def get_name(self, obj: Dataset):
        return obj.label

    def get_identifier(self, obj: Dataset):
        return obj.uuid

    def get_last_update(self, obj: Dataset):
        if obj.last_update:
            return obj.last_update
        return ''
