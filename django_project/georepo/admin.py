import os.path
import math
import zipfile
import tempfile

from django.contrib import admin
from django.conf import settings
from django.http import HttpResponse
from django.utils.html import format_html
from guardian.admin import GuardedModelAdmin
from georepo.models import (
    GeographicalEntity,
    Language,
    EntityType,
    EntityName,
    Dataset,
    CodeCL,
    EntityCode,
    LayerStyle,
    DatasetTilingConfig,
    EntityTypeTilingConfig
)


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


class GeographicalEntityAdmin(admin.ModelAdmin):
    list_display = (
        'label', 'level', 'type'
    )
    list_filter = (
        'level', 'type'
    )
    search_fields = (
        'label',
    )
    raw_id_fields = (
        'parent',
    )

    def get_queryset(self, request):
        return GeographicalEntity.objects.filter(id__gte=0)


@admin.action(description='Generate vector tiles')
def generate_vector_tiles(modeladmin, request, queryset):
    from dashboard.tasks import generate_vector_tiles_task
    for dataset in queryset:
        task = generate_vector_tiles_task.delay(dataset.id, True)
        dataset.task_id = task.id
        dataset.save()


@admin.action(description='Export geojson data')
def export_geojson_data(modeladmin, request, queryset):
    from georepo.utils.geojson import generate_geojson
    geojson_files = []
    for dataset in queryset:
        geojson_file_path = generate_geojson(dataset)
        geojson_files.append(geojson_file_path)

    if geojson_files:
        with tempfile.SpooledTemporaryFile() as tmp_file:
            with zipfile.ZipFile(
                    tmp_file, 'w', zipfile.ZIP_DEFLATED) as archive:
                for geojson_file in geojson_files:
                    archive.write(
                        geojson_file,
                        arcname=geojson_file.split('/')[-1])
            tmp_file.seek(0)
            response = HttpResponse(
                tmp_file.read(), content_type='application/x-zip-compressed'
            )
            response['Content-Disposition'] = (
                'attachment; filename="geojson.zip"'
            )
            return response


def generate_geojson_data(modeladmin, request, queryset):
    from dashboard.tasks import generate_dataset_export_data
    for dataset in queryset:
        generate_dataset_export_data.delay(dataset.id)


class DatasetAdmin(GuardedModelAdmin):
    list_display = (
        'label', 'size', 'tiling_status', 'geojson', 'layer_preview')
    actions = [
        generate_vector_tiles, export_geojson_data, generate_geojson_data]

    def geojson(self, obj: Dataset):
        geojson_file_path = os.path.join(
            settings.GEOJSON_FOLDER_OUTPUT,
            obj.label
        ) + '.geojson'
        if os.path.exists(geojson_file_path):
            return format_html(
                '<a href="{}">GeoJSON File</a>'.format(
                    geojson_file_path.replace(
                        settings.MEDIA_ROOT,
                        settings.MEDIA_URL
                    )))
        return '-'


    def layer_preview(self, obj: Dataset):
        tile_path = os.path.join(
            settings.LAYER_TILES_PATH,
            obj.label
        )
        if os.path.exists(tile_path):
            return format_html(
                '<a href="/layer-test/?dataset={}">Layer Preview</a>'.format(
                    obj.label))
        return '-'

    def tiling_status(self, obj: Dataset):
        if obj.task_id:
            from celery.result import AsyncResult
            res = AsyncResult(obj.task_id)
            return 'Done' if res.ready() else 'Processing'
        return '-'

    def size(self, obj: Dataset):
        tile_path = os.path.join(
            settings.LAYER_TILES_PATH,
            obj.label
        )
        if os.path.exists(tile_path):
            folder_size = 0
            # get size
            for path, dirs, files in os.walk(tile_path):
                for f in files:
                    fp = os.path.join(path, f)
                    folder_size += os.stat(fp).st_size

            return convert_size(folder_size)

        return '0'


class LayerStyleAdmin(admin.ModelAdmin):
    list_display = ('label', 'dataset', 'level', 'type')


class EntityTilingConfigInline(admin.TabularInline):
    model = EntityTypeTilingConfig
    extra = 0


class DatasetTilingConfigAdmin(admin.ModelAdmin):
    list_display = (
        'dataset', 'zoom_level'
    )
    inlines = [
        EntityTilingConfigInline,
    ]


admin.site.register(GeographicalEntity, GeographicalEntityAdmin)
admin.site.register(Language)
admin.site.register(EntityType)
admin.site.register(EntityName)
admin.site.register(CodeCL)
admin.site.register(EntityCode)
admin.site.register(Dataset, DatasetAdmin)
admin.site.register(LayerStyle, LayerStyleAdmin)
admin.site.register(DatasetTilingConfig, DatasetTilingConfigAdmin)
