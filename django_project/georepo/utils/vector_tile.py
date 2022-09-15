import shutil
import subprocess
import logging
import toml
import os
import time

from django.conf import settings
from core.settings.utils import absolute_path
from georepo.models import Dataset

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def dataset_sql_query(dataset_id, level, tolerance=None):
    if tolerance:
        select_sql = (
            'SELECT ST_AsBinary(ST_SimplifyVW(gg.geometry, '
            '{tolerance})) AS geometry, '.format(
                tolerance=tolerance
            )
        )
    else:
        select_sql = 'SELECT ST_AsBinary(gg.geometry) AS geometry, '
    sql = (
        select_sql +
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
            dataset_id=dataset_id
        ))
    return sql


def create_configuration_files(dataset: Dataset) -> [str]:
    """
    Create multiple toml configuration files based on dataset tiling config
    :return: array of output path
    """
    from georepo.models.dataset_tile_config import (
        DatasetTilingConfig
    )

    template_config_file = absolute_path(
        'georepo', 'utils', 'config.toml'
    )
    dataset_tiling_conf = DatasetTilingConfig.objects.filter(
        dataset=dataset
    )
    toml_dataset_filepaths = []

    for dataset_conf in dataset_tiling_conf:
        toml_data = toml.load(template_config_file)
        toml_dataset_filepath = os.path.join(
            '/',
            'opt',
            'tegola_config',
            f'dataset-{dataset.id}-{dataset_conf.zoom_level}.toml'
        )

        entity_confs = dataset_conf.entitytypetilingconfig_set.all()
        toml_data['maps'] = [{
            'name': f'temp_{dataset.label}',
            'layers': []
        }]

        for entity_conf in entity_confs:
            try:
                level = entity_conf.entity_type.geographicalentity_set.filter(
                    dataset=dataset).first().level
            except Exception:  # noqa
                level = 0
            sql = dataset_sql_query(
                dataset.id,
                level,
                tolerance=entity_conf.simplify_tolerance
            )
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
        toml_dataset_filepaths.append({
            'zoom': dataset_conf.zoom_level,
            'config_file': toml_dataset_filepath
        })

    return toml_dataset_filepaths


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
        'name': f'temp_{dataset.label}',
        'layers': []
    }]

    for level in levels:
        sql = dataset_sql_query(
            dataset.id,
            level
        )
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
    from georepo.utils import generate_geojson
    if dataset.datasettilingconfig_set.exists():
        toml_config_files = create_configuration_files(dataset)
    else:
        toml_config_file = create_configuration_file(dataset)
        toml_config_files = [{
            'config_file': toml_config_file
        }]

    bounds = None

    level_0_entity = dataset.geographicalentity_set.filter(level=0)
    if level_0_entity.exists() and level_0_entity.count() == 1:
        bounds = (
            ','.join([str(x) for x in level_0_entity.first().geometry.extent])
        )

    for toml_config_file in toml_config_files:
        command_list = (
            [
                '/opt/tegola',
                'cache',
                'seed',
                '--config',
                toml_config_file['config_file'],
                '--overwrite' if overwrite else '',
            ]
        )
        if bounds:
            command_list.extend([
                '--bounds',
                bounds])

        if 'zoom' in toml_config_file:
            command_list.extend([
                '--min-zoom',
                str(toml_config_file['zoom']),
                '--max-zoom',
                str(toml_config_file['zoom'])
            ])
        else:
            command_list.extend([
                '--min-zoom',
                '1',
                '--max-zoom',
                '8'
            ])
        subprocess.run(command_list)
    original_vector_tile_path = os.path.join(
        settings.LAYER_TILES_PATH,
        dataset.label
    )
    if os.path.exists(original_vector_tile_path):
        shutil.rmtree(original_vector_tile_path)

    shutil.move(
        os.path.join(
            settings.LAYER_TILES_PATH,
            f'temp_{dataset.label}'
        ),
        original_vector_tile_path
    )

    dataset.vector_tiles_path = (
        f'/layer_tiles/{dataset.label}/{{z}}/{{x}}/{{y}}?t={int(time.time())}'
    )
    dataset.save()

    logger.info('Extracting geojson from {}'.format(dataset.label))
    generate_geojson(dataset)

    logger.info('Generating vector tiles done...')
