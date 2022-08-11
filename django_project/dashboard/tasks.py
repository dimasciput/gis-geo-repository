from celery import shared_task

from dashboard.models import (
    LayerUploadSession, ERROR, DONE
)
from georepo.models import EntityType
from georepo.utils import load_geojson


@shared_task(name="process_layer_upload_session")
def process_layer_upload_session(layer_upload_session_id: str):

    layer_upload_session = LayerUploadSession.objects.get(
        id=layer_upload_session_id
    )
    for layer_file in layer_upload_session.layerfile_set.all().order_by(
            'level'):
        entity_type, _ = EntityType.objects.get_or_create(
            label=layer_file.entity_type
        )
        loaded, message = load_geojson(
            layer_file.layer_file.path,
            int(layer_file.level),
            entity_type,
            layer_upload_session.layer_name_format,
            layer_upload_session.dataset,
            layer_upload_session.layer_code_format,
            layer_upload_session.id
        )
        if loaded:
            layer_file.processed = True
            layer_file.save()
        else:
            layer_upload_session = (
                LayerUploadSession.objects.get(id=layer_upload_session.id)
            )
            layer_upload_session.status = ERROR
            layer_upload_session.message = message
            layer_upload_session.save()
            return
    layer_upload_session = (
        LayerUploadSession.objects.get(id=layer_upload_session.id)
    )
    layer_upload_session.status = DONE
    layer_upload_session.save()


@shared_task(name="generate_vector_tiles")
def generate_vector_tiles_task(dataset_id: str, overwrite: bool):
    from georepo.models.dataset import Dataset
    from georepo.utils.vector_tile import generate_vector_tiles

    try:
        dataset = Dataset.objects.get(id=dataset_id)
        generate_vector_tiles(dataset, overwrite)
    except Dataset.DoesNotExist:
        return
