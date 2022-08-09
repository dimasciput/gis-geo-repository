from django.urls import path, re_path
from django.views.generic import TemplateView

from georepo.api_views.reference_layer_list import (
    ReferenceLayerList
)
from georepo.api_views.reference_layer import (
    ReferenceLayerGeojson,
    ReferenceLayerEntityList,
    ReferenceLayerDetail,
    ReferenceLayerHierarchical
)
from georepo.api_views.protected_api import IsDatasetAllowedAPI

urlpatterns = [
    path('layer-test/', TemplateView.as_view(
        template_name='test_layer.html'
    )),
    re_path(
        r'api/reference-layer/(?P<uuid>[\da-f-]+)/(?P<entity_type>\w+)/?$',
        ReferenceLayerGeojson.as_view(),
        name='reference-layer-geojson'),
    re_path(
        r'api/reference-layer/(?P<uuid>[\da-f-]+)/'
        r'(?P<entity_type>\w+)/list/?$',
        ReferenceLayerEntityList.as_view(),
        name='reference-layer-entity-list'),
    re_path(
        r'api/reference-layer/(?P<uuid>[\da-f-]+)/?$',
        ReferenceLayerDetail.as_view(),
        name='reference-layer-detail'),
    re_path(
        r'api/reference-layer/list/?$',
        ReferenceLayerList.as_view(),
        name='reference-layer-list'),
    re_path(
        r'api/reference-layer/hierarchical/(?P<uuid>[\da-f-]+)/?$',
        ReferenceLayerHierarchical.as_view(),
        name='reference-layer-hierarchical'
    ),
    re_path(
        r'api/protected/?$',
        IsDatasetAllowedAPI.as_view(),
        name='dataset-allowed-api'
    ),
]
