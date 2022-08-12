import json
import random
from django.views.generic import TemplateView
from django.conf import settings

from georepo.models import Dataset
from georepo.models.dataset_tile_config import EntityTypeTilingConfig


class LayerTestView(TemplateView):
    template_name = 'test_layer.html'

    def get_context_data(self, **kwargs):
        ctx = super(LayerTestView, self).get_context_data(**kwargs)
        dataset_string = self.request.GET.get('dataset')
        if not dataset_string:
            return ctx
        dataset = Dataset.objects.filter(
            label__iexact=dataset_string
        ).first()
        entity = dataset.geographicalentity_set.filter(
            level=0
        ).first()
        ctx['dataset'] = dataset
        ctx['layer_tiles_base_url'] = settings.LAYER_TILES_BASE_URL
        ctx['center'] = json.loads(entity.geometry.centroid.json)
        ctx['layers_configs'] = []
        levels = dataset.geographicalentity_set.values_list(
            'level', flat=True).order_by('-level').distinct()
        for level in levels:
            entity_type = dataset.geographicalentity_set.filter(
                level=level
            ).first().type
            color = "#" + (
                ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            )
            layers_config = {
                'id': entity_type.label.lower(),
                'source': dataset.label,
                'source-layer': f'Level-{level}',
                'type': 'line',
                'paint': {
                    'line-color': color,
                    'line-width': 1
                }
            }
            entity_conf = EntityTypeTilingConfig.objects.filter(
                entity_type=entity_type,
                dataset_tiling_config__dataset=dataset
            ).order_by('dataset_tiling_config__zoom_level')
            if entity_conf.exists():
                layers_config['minzoom'] = (
                    entity_conf.first().dataset_tiling_config.zoom_level
                )
                layers_config['maxzoom'] = (
                    entity_conf.last().dataset_tiling_config.zoom_level
                )
            else:
                layers_config['minzoom'] = 1
                layers_config['maxzoom'] = 8

            ctx['layers_configs'].append(layers_config)
        return ctx
