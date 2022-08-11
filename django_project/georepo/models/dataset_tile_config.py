from django.db import models


class DatasetTilingConfig(models.Model):

    dataset = models.ForeignKey(
        'georepo.Dataset',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    zoom_level = models.IntegerField(
        null=False,
        blank=False,
        default=0
    )

    def __str__(self):
        return '{0} - {1}'.format(
            self.dataset.label,
            self.zoom_level
        )

    class Meta:
        ordering = [
            'dataset__label',
            'zoom_level'
        ]


class EntityTypeTilingConfig(models.Model):

    dataset_tiling_config = models.ForeignKey(
        'georepo.DatasetTilingConfig',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    entity_type = models.ForeignKey(
        'georepo.EntityType',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    simplify_tolerance = models.FloatField(
        default=0
    )

    def __str__(self):
        return '{0} - {1}'.format(
            self.dataset_tiling_config,
            self.entity_type.label
        )
