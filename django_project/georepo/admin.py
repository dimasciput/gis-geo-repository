import os.path
import math

from django.contrib import admin
from django.conf import settings
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


class DatasetAdmin(GuardedModelAdmin):
    list_display = ('label', 'size', 'tiling_status')
    actions = [generate_vector_tiles]

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
