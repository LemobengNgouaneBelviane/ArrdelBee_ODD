import csv
import re
import os
from django.core.management.base import BaseCommand
from odd.models import SDG, SDGTarget, SDGIndicator, SND30Axis

class Command(BaseCommand):
    help = 'Import ODD and SND30 data from CSV'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            type=str,
            default=None,
            help='Chemin vers le fichier CSV ODD (ex: /chemin/vers/odd.csv)',
        )

    def handle(self, *args, **options):
        self.import_sdgs(options.get('csv'))
        self.import_snd30()

    def import_sdgs(self, csv_path=None):
        if not csv_path:
            # Chemin par défaut relatif à la racine du projet
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            csv_path = os.path.join(base_dir, "ODD, Objctifs, Cibles et Indicateurs 082023(1).csv")

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'CSV file not found at {csv_path}'))
            self.stdout.write(self.style.WARNING('Utilisez --csv /chemin/vers/fichier.csv pour spécifier le chemin.'))
            return

        self.stdout.write('Importing SDGs...')
        
        current_sdg = None
        current_target = None
        
        # Consistent colors for SDGs
        SDG_COLORS = {
            1: "#E5243B", 2: "#DDA63A", 3: "#4C9F38", 4: "#C5192D",
            5: "#FF3A21", 6: "#26BDE2", 7: "#FCC30B", 8: "#A21942",
            9: "#FD6925", 10: "#DD1367", 11: "#FD9D24", 12: "#BF8B2E",
            13: "#3F7E44", 14: "#0A97D9", 15: "#56C02B", 16: "#00689D",
            17: "#19486A"
        }

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or not row[0].strip():
                    continue
                
                line = row[0].strip().strip('"').strip()
                
                # ODD Objective
                obj_match = re.match(r'^Objectif\s+(\d+)\.\s+(.+)$', line)
                if obj_match:
                    num = int(obj_match.group(1))
                    name = obj_match.group(2)
                    current_sdg, _ = SDG.objects.update_or_create(
                        number=num,
                        defaults={'name': name, 'color': SDG_COLORS.get(num, "#000000")}
                    )
                    current_target = None
                    continue
                
                # Indicator
                indicator_match = re.match(r'^(\d+\.[0-9a-z]+(?:\.[0-9a-z]+)+)(?:\s+|-|)(.*)$', line, re.IGNORECASE)
                if indicator_match and current_target:
                    code = indicator_match.group(1).lower()
                    desc = indicator_match.group(2).strip()
                    SDGIndicator.objects.update_or_create(
                        code=code,
                        defaults={'description': desc, 'target': current_target}
                    )
                    continue

                # Target
                target_match = re.match(r'^(\d+\.[0-9a-z]+)(?:\s+|-|)(.*)$', line, re.IGNORECASE)
                if target_match and current_sdg:
                    code = target_match.group(1).lower()
                    desc = target_match.group(2).strip()
                    current_target, _ = SDGTarget.objects.update_or_create(
                        code=code,
                        defaults={'description': desc, 'sdg': current_sdg}
                    )
                    continue

        self.stdout.write(self.style.SUCCESS('SDGs imported successfully'))

    def import_snd30(self):
        self.stdout.write('Importing SND30 Axes...')
        
        AXES = [
            (1, 'Renforcement des institutions démocratiques', 'Gouvernance démocratique et développement institutionnel'),
            (2, 'Développement équitable et inclusif', 'Réduction des inégalités et inclusion sociale'),
            (3, 'Croissance durable et compétitivité', 'Croissance économique et développement du secteur privé'),
            (4, 'Capital naturel et résilience climatique', 'Protection environnementale et action climatique'),
            (5, 'Paix et sécurité', 'Cohésion sociale et prévention des conflits'),
        ]

        for num, name, desc in AXES:
            SND30Axis.objects.update_or_create(
                number=num,
                defaults={'name': name, 'description': desc}
            )

        self.stdout.write(self.style.SUCCESS('SND30 Axes imported successfully'))
