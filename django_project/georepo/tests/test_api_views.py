import uuid
import mock

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIRequestFactory

from georepo.api_views.reference_layer import (
    ReferenceLayerDetail,
    ReferenceLayerEntityList,
    ReferenceLayerHierarchical
)
from georepo.api_views.protected_api import IsDatasetAllowedAPI
from georepo.tests.model_factories import (
    GeographicalEntityF, EntityTypeF, DatasetF, UserF
)


class TestApiViews(TestCase):

    def setUp(self) -> None:
        self.entity_type = EntityTypeF.create(label='Country')
        self.dataset = DatasetF.create()
        self.entity = GeographicalEntityF.create(
            uuid=str(uuid.uuid4()),
            type=self.entity_type,
            level=0,
            dataset=self.dataset,
            internal_code='GO'
        )
        self.factory = APIRequestFactory()

    @mock.patch('georepo.api_views.protected_api.IsDatasetAllowedAPI.has_perm',
                mock.Mock(side_effect=[True]))
    def test_is_dataset_allowed_api(self):
        user = UserF.create(username='test')

        # Without request url
        request = self.factory.post(
            reverse('dataset-allowed-api') +
            f'?token={str(user.auth_token)}'
        )
        view = IsDatasetAllowedAPI.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 403)

        request = self.factory.post(
            reverse('dataset-allowed-api') +
            f'?token={str(user.auth_token)}' +
            f'&request_url=/t/{self.dataset.label}/City/'
        )
        view = IsDatasetAllowedAPI.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_get_reference_layer_detail(self):
        kwargs = {
            'uuid': self.entity.uuid
        }
        request = self.factory.get(
            reverse('reference-layer-detail', kwargs=kwargs)
        )
        view = ReferenceLayerDetail.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_get_reference_layer_list(self):
        entity_type = EntityTypeF.create(label='District')
        GeographicalEntityF.create(
            uuid=str(uuid.uuid4()),
            type=entity_type,
            level=1,
            dataset=self.dataset
        )
        kwargs = {
            'uuid': self.entity.uuid,
            'entity_type': entity_type
        }
        request = self.factory.get(
            reverse('reference-layer-list')
        )
        view = ReferenceLayerEntityList.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_get_hierarchical_data(self):
        GeographicalEntityF.create(
            uuid=str(uuid.uuid4()),
            level=1,
            dataset=self.dataset,
            internal_code='GO2',
            parent=self.entity
        )
        kwargs = {
            'uuid': self.entity.uuid
        }
        request = self.factory.get(
            reverse('reference-layer-hierarchical', kwargs=kwargs)
        )
        view = ReferenceLayerHierarchical.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('GO' in response.data)
