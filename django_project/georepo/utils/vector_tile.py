import subprocess
import logging
import toml
import os
import time

from core.settings.utils import absolute_path
from georepo.models import Dataset

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def create_configuration_file(dataset: Dataset) -> str:
    """
    Create toml configuration file that will be used for tegola
    :return: output path
    """

    template_config_file = absolute_path(
        'georepo', 'utils', 'config.toml'
    )
    toml_data = toml.load(template_config_file)
    toml_dataset_filepath = os.path.join(
        '/',
        'opt',
        'tegola_config',
        f'dataset-{dataset.id}.toml'
    )

    entities = dataset.geographicalentity_set.all().order_by('level')
    levels = entities.values_list('level', flat=True).distinct()
    toml_data['maps'] = [{
        'name': dataset.label,
        'layers': []
    }]

    for level in levels:
        sql = (
            'SELECT ST_AsBinary(gg.geometry) AS geometry, '
            'ST_AsText(circle.center) AS centroid, '
            'gg.id, gg.label, '
            'gg.level, ge.label as type, gg.internal_code as code,'
            'pg.internal_code as parent_code '
            'FROM georepo_geographicalentity gg '
            'INNER JOIN georepo_entitytype ge on ge.id = gg.type_id '
            'LEFT JOIN georepo_geographicalentity pg on pg.id = gg.parent_id '
            'LEFT JOIN LATERAL (SELECT * from ST_MaximumInscribedCircle(gg.geometry)) circle ON True '  # noqa
            'WHERE gg.geometry && !BBOX! and gg.level = {level} '
            'AND gg.dataset_id = {dataset_id}'.
            format(
                level=level,
                dataset_id=dataset.id
            ))
        provider_layer = {
            'name': f'Level-{level}',
            'geometry_fieldname': 'geometry',
            'id_fieldname': 'id',
            'sql': sql,
            'srid': 4326
        }
        if 'layers' not in toml_data['providers'][0]:
            toml_data['providers'][0]['layers'] = []
        toml_data['providers'][0]['layers'].append(
            provider_layer
        )
        toml_data['maps'][0]['layers'].append({
            'provider_layer': f'docker_postgis.{provider_layer["name"]}'
        })

    toml_dataset_file = open(toml_dataset_filepath, 'w')
    toml_dataset_file.write(
        toml.dumps(toml_data)
    )
    toml_dataset_file.close()

    return toml_dataset_filepath


def generate_vector_tiles(dataset: Dataset, overwrite: bool = False):
    toml_config_file = create_configuration_file(dataset)
    bounds = (
        ','.join([str(x) for x in dataset.geographicalentity_set.filter(
            level=0).first().geometry.extent])
    )
    subprocess.Popen(
        [
            '/opt/tegola',
            'cache',
            'seed',
            '--config',
            toml_config_file,
            '--bounds',
            bounds,
            '--min-zoom',
            '1',
            '--max-zoom',
            '8',
            '--overwrite' if overwrite else '',
        ]
    )
    dataset.vector_tiles_path = (
        f'/layer_tiles/{dataset.label}/{{z}}/{{x}}/{{y}}?t={int(time.time())}'
    )
    dataset.save()
