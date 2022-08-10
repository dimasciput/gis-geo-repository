import fiona
import json

from django.contrib.gis.geos import GEOSGeometry, Polygon, MultiPolygon

from georepo.models import GeographicalEntity, EntityType, Dataset


def load_gpkg_file(
        file_path: str,
        level: int,
        entity_type: EntityType,
        name_field: str,
        code_field: str = None,
        dataset: str = None,
        limit: int = None):
    layers = fiona.listlayers(file_path)

    entity_added = 0
    entity_updated = 0

    if not layers:
        return False
    layer_name = layers[0]

    index = 0

    if dataset:
        dataset, _ = Dataset.objects.get_or_create(
            label=dataset
        )

    with fiona.open(file_path, layer=layer_name) as layer:
        for feature in layer:
            properties = feature['properties']
            geom_str = json.dumps(feature['geometry'])
            geom = GEOSGeometry(geom_str)
            if isinstance(geom, Polygon):
                geom = MultiPolygon([geom])
            if not isinstance(geom, MultiPolygon):
                raise TypeError(
                    'Type is not acceptable'
                )
            label = name_field.format(level=level)
            code = code_field.format(level=level)

            if label not in properties or code not in properties:
                return False, 'Label or code format not found in the layer'

            feature_label = properties[label]
            if not feature_label:
                feature_label = properties[code]

            entity, created = GeographicalEntity.objects.update_or_create(
                label=feature_label,
                type=entity_type,
                internal_code=properties[code],
                defaults={
                    'geometry': geom,
                    'dataset': dataset,
                    'level': level,
                }
            )

            if created:
                entity_added += 1
            else:
                entity_updated += 1

            if level > 0:
                try:
                    parent_code_field = code_field.format(
                        level=level - 1
                    )
                    parent = GeographicalEntity.objects.get(
                        internal_code__iexact=properties[parent_code_field],
                        level=level - 1
                    )
                    entity.parent = parent
                    entity.save()
                except (KeyError, GeographicalEntity.DoesNotExist):
                    pass

            print('{0} - {1} {2}'.format(
                properties[code],
                feature_label,
                'Added' if created else 'Updated'))

            index += 1

            if limit and index > limit:
                return True, 'Reached limit'

        print('Entities updated : {}'.format(entity_updated))
        print('Entities added : {}'.format(entity_added))

        return True, ''
