import json
import os
from django.core.management.base import BaseCommand
from odd.models import GaddDimension, GaddTheme, GaddObjective


class Command(BaseCommand):
    help = "Import le référentiel GADD (6 dimensions, thèmes, 166 objectifs officiels)."

    def add_arguments(self, parser):
        parser.add_argument(
            '--json',
            type=str,
            default=None,
            help='Chemin vers le fichier JSON du référentiel (défaut : odd/data/gadd_referentiel.json)',
        )

    def handle(self, *args, **options):
        json_path = options.get('json')
        if not json_path:
            json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'gadd_referentiel.json')

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f'Fichier introuvable : {json_path}'))
            return

        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)

        dim_count = theme_count = obj_count = 0

        for key, dim_data in data.items():
            dimension, _ = GaddDimension.objects.update_or_create(
                key=key,
                defaults={
                    'label': dim_data['label'],
                    'description': dim_data['description'],
                    'order': dim_data['order'],
                },
            )
            dim_count += 1

            for theme_data in dim_data['themes']:
                theme, _ = GaddTheme.objects.update_or_create(
                    dimension=dimension,
                    number=theme_data['number'],
                    defaults={'label': theme_data['label']},
                )
                theme_count += 1

                for obj_data in theme_data['objectives']:
                    GaddObjective.objects.update_or_create(
                        theme=theme,
                        code=obj_data['code'],
                        defaults={'label': obj_data['label']},
                    )
                    obj_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'{dim_count} dimensions, {theme_count} thèmes, {obj_count} objectifs importés.'
        ))
