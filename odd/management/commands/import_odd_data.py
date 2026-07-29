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

        PILIER1 = "Transformation structurelle de l'économie"
        PILIER2 = "Développement du capital humain et du bien-être"
        PILIER3 = "Promotion de l'emploi et de l'insertion économique"
        PILIER4 = "Gouvernance, décentralisation et gestion stratégique de l'État"

        # Piliers et axes d'intervention officiels de la SND30 2020-2030.
        # Le pilier 4 ne dispose pas d'une liste d'axes distincte dans le
        # document source (erreur de mise en page dupliquant le pilier 3) :
        # il est donc représenté par un axe unique correspondant à son intitulé.
        AXES = [
            (1, 1, PILIER1, "Développement des industries et des services",
             "Promotion de l'industrie manufacturière et rattrapage technologique ; "
             "filières prioritaires : énergie, agro-industrie, numérique, forêt-bois, "
             "textile-confection-cuir, mines-métallurgie, hydrocarbures, chimie-pharmacie, "
             "construction-services"),
            (2, 1, PILIER1, "Développement de la productivité et de la production agricoles",
             "Amélioration des rendements agricoles, de la production vivrière et de l'agro-industrie"),
            (3, 1, PILIER1, "Développement des infrastructures productives",
             "Infrastructures de transport, d'énergie et de numérique au service de la production"),
            (4, 1, PILIER1, "Intégration régionale et facilitation des échanges",
             "Renforcement des échanges commerciaux régionaux et de l'intégration économique sous-régionale"),
            (5, 1, PILIER1, "Dynamisation du secteur privé",
             "Amélioration du climat des affaires et soutien à l'investissement privé"),
            (6, 1, PILIER1, "Préservation de l'environnement et protection de la nature",
             "Gestion durable des ressources naturelles et lutte contre les changements climatiques"),
            (7, 1, PILIER1, "Transformation du système financier",
             "Modernisation du secteur financier et amélioration de l'accès au financement"),

            (8, 2, PILIER2, "Amélioration de l'éducation, formation et employabilité",
             "Accès à une éducation de qualité et adéquation formation-emploi"),
            (9, 2, PILIER2, "Santé et nutrition",
             "Amélioration de l'état de santé et nutritionnel des populations, couverture santé universelle"),
            (10, 2, PILIER2, "Promotion de l'accès aux facilités sociales de base",
             "Accès à l'eau, à l'assainissement, au logement et aux services sociaux essentiels"),
            (11, 2, PILIER2, "Amélioration de la protection sociale",
             "Renforcement des dispositifs de protection sociale et d'assistance aux populations vulnérables"),
            (12, 2, PILIER2, "Promotion de la recherche-développement et de l'innovation",
             "Développement de la recherche scientifique et de l'innovation technologique"),

            (13, 3, PILIER3, "Promotion de l'emploi dans les projets d'investissement public",
             "Création d'emplois locaux à travers les projets d'investissement public"),
            (14, 3, PILIER3, "Amélioration de la productivité agricole, de l'emploi et des revenus en milieu rural",
             "Développement économique rural et amélioration des revenus agricoles"),
            (15, 3, PILIER3, "Promotion de la migration de l'informel vers le formel",
             "Formalisation des activités économiques informelles"),
            (16, 3, PILIER3, "Création et préservation de l'emploi décent dans les grandes entreprises",
             "Emploi décent et stable dans le secteur formel"),
            (17, 3, PILIER3, "Mise en adéquation formation-emploi et insertion professionnelle",
             "Adaptation des formations aux besoins du marché du travail"),
            (18, 3, PILIER3, "Régulation du marché du travail",
             "Encadrement et régulation des relations et conditions de travail"),

            (19, 4, PILIER4, "Gouvernance, décentralisation et gestion stratégique de l'État",
             "Renforcement de la gouvernance publique, décentralisation et transferts de compétences aux CTD"),
        ]

        for num, pilier_number, pilier_title, name, desc in AXES:
            SND30Axis.objects.update_or_create(
                number=num,
                defaults={
                    'name': name, 'description': desc,
                    'pilier_number': pilier_number, 'pilier_title': pilier_title,
                }
            )

        # Retire les anciens axes (1 à 5, obsolètes) si l'ancien jeu de données
        # avait déjà été importé et que leur numéro ne correspond plus à un axe valide.
        valid_numbers = [a[0] for a in AXES]
        SND30Axis.objects.exclude(number__in=valid_numbers).delete()

        self.stdout.write(self.style.SUCCESS('SND30 Axes imported successfully'))
