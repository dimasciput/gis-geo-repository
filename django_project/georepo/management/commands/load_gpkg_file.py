from django.core.management import BaseCommand

from georepo.models import EntityType
from georepo.utils.gpkg_file import load_gpkg_file


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--gpkg_file',
            required=True
        )
        parser.add_argument(
            '--level'
        )
        parser.add_argument(
            '--limit'
        )
        parser.add_argument(
            '--name_field'
        )
        parser.add_argument(
            '--code_field'
        )
        parser.add_argument(
            '--dataset'
        )
        parser.add_argument(
            '--type',
            required=True
        )
        parser.add_argument(
            '--parent_field'
        )

    def handle(self, *args, **options):

        entity_type, created = EntityType.objects.get_or_create(
            label=options['type']
        )
        limit = options['limit']
        if limit:
            limit = int(limit)

        gpkg_loaded, message = load_gpkg_file(
            options['gpkg_file'],
            int(options['level']),
            entity_type,
            options['name_field'],
            options['code_field'],
            options['dataset'],
            limit
        )

        print('Geojson loaded : {}'.format(gpkg_loaded))
