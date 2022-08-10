from georepo.api_views.api_cache import ApiCache
from georepo.models import Dataset
from georepo.serializers.dataset import DatasetSerializer


class ReferenceLayerList(ApiCache):
    """
    View to list all reference layers in the system
    """
    cache_model = Dataset

    def get_response_data(self, request, *args, **kwargs):
        datasets = Dataset.objects.all()
        serializer = DatasetSerializer(
            datasets,
            many=True
        )
        return serializer.data
