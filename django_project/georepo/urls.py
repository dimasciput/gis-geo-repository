from django.urls import path, re_path

from georepo.api_views.reference_layer_list import (
    ReferenceLayerList
)
from georepo.api_views.reference_layer import (
    ReferenceLayerGeojson,
    ReferenceLayerEntityList,
    ReferenceLayerDetail,
    ReferenceLayerHierarchical,
    ReferenceLayerGeojsonDownload
)
from georepo.views.layer_test import LayerTestView
from georepo.api_views.protected_api import IsDatasetAllowedAPI

urlpatterns = [
    path('layer-test/', LayerTestView.as_view()),
    re_path(
        r'api/reference-layer/(?P<uuid>[\da-f-]+)/geojson/?$',
        ReferenceLayerGeojsonDownload.as_view(),
        name='reference-layer-geojson-download'),
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
