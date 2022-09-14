from uuid import uuid4

from django.conf import settings
from django.contrib.gis.db import models


class GeographicalEntity(models.Model):
    id = models.AutoField(primary_key=True)

    dataset = models.ForeignKey(
        'georepo.Dataset',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    uuid = models.UUIDField(
        default=uuid4
    )

    uuid_versioned = models.UUIDField(
        primary_key=False,
        default=uuid4
    )

    internal_code = models.CharField(
        null=True,
        blank=True,
        max_length=255
    )

    level = models.IntegerField(
        default=0
    )

    label = models.CharField(
        null=True,
        blank=True,
        max_length=255
    )

    start_date = models.DateTimeField(
        null=True,
        blank=True
    )

    end_date = models.DateTimeField(
        null=True,
        blank=True
    )

    is_latest = models.BooleanField(
        null=True,
        blank=True,
    )

    is_approved = models.BooleanField(
        null=True,
        blank=True
    )

    is_private = models.BooleanField(
        default=False
    )

    approved_date = models.DateTimeField(
        null=True,
        blank=True
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    geometry = models.MultiPolygonField(
        null=True
    )

    source = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    source_url = models.URLField(
        null=True,
        blank=True
    )

    license = models.TextField(
        null=True,
        blank=True
    )

    qc_notes = models.TextField(
        verbose_name='QC Notes',
        null=True,
        blank=True
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )

    type = models.ForeignKey(
        'georepo.EntityType',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    class Meta:
        verbose_name_plural = 'Geographical Entities'

    def __str__(self):
        return self.label

    def get_all_children(self):
        children = [self]
        try:
            child_list = self.children.all()
        except AttributeError:
            return children
        for child in child_list:
            children.extend(child.get_all_children())
        return children


class EntityName(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(
        blank=False,
        null=False,
        max_length=255
    )

    geographical_entity = models.ForeignKey(
        'georepo.GeographicalEntity',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    language = models.ForeignKey(
        'georepo.Language',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


class EntityType(models.Model):
    id = models.AutoField(primary_key=True)

    label = models.CharField(
        help_text='Examples: Country, Region, etc.',
        blank=False,
        null=False,
        max_length=255
    )

    def __str__(self):
        return self.label
