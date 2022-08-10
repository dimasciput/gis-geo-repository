import math

from rest_framework.generics import get_object_or_404
from django.core.paginator import Paginator

from georepo.api_views.api_cache import ApiCache
from georepo.models import GeographicalEntity, Dataset
from georepo.serializers.entity import (
    GeographicalGeojsonSerializer,
    GeographicalEntitySerializer,
    DetailedEntitySerializer
)


class ReferenceLayerDetail(ApiCache):
    """
    API to get reference layer detail
    """
    cache_model = Dataset

    def get_response_data(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid', None)
        dataset = get_object_or_404(
            Dataset, uuid=uuid
        )
        response_data = (
            DetailedEntitySerializer(dataset).data
        )
        return response_data


class ReferenceLayerEntityList(ApiCache):
    """
    Reference layer list per entity type
    """
    cache_model = Dataset

    def get_serializer(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return GeographicalEntitySerializer

    def get_response_data(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid', None)
        entity_type = kwargs.get('entity_type', None)
        page = int(request.GET.get('page', '1'))
        page_size = int(request.GET.get('page_size', '50'))

        entities = GeographicalEntity.objects.filter(
            dataset__uuid=uuid
        )
        if entity_type:
            entities = entities.filter(
                type__label=entity_type
            )

        paginator = Paginator(entities, page_size)
        total_page = math.ceil(paginator.count / page_size)
        if page > total_page:
            output = []
        else:
            paginated_entities = paginator.get_page(page)
            output = (
                self.get_serializer()(
                    paginated_entities, many=True).data
            )
        return {
            'page': page,
            'total_page': total_page,
            'page_size': page_size,
            'results': output
        }


class ReferenceLayerGeojson(ReferenceLayerEntityList):
    """
    Reference Layer in Geojson.
    """
    def get_serializer(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return GeographicalGeojsonSerializer


class ReferenceLayerHierarchical(ApiCache):
    cache_model = Dataset

    def entities_code(self, parent_entity: GeographicalEntity):
        codes = []
        entities = GeographicalEntity.objects.filter(
            parent=parent_entity
        ).order_by('internal_code')
        for entity in entities:
            if GeographicalEntity.objects.filter(parent=entity).exists():
                codes.append({
                    entity.internal_code: self.entities_code(entity)
                })
            else:
                codes.append(entity.internal_code)
        return codes

    def get_response_data(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid', None)
        codes = []
        try:
            dataset = Dataset.objects.get(uuid=uuid)
        except Dataset.DoesNotExist:
            return []

        highest_entities = GeographicalEntity.objects.filter(
            level=0,
            dataset=dataset
        )

        for entity in highest_entities:
            codes.append({
                entity.internal_code: self.entities_code(entity)
            })

        return codes
