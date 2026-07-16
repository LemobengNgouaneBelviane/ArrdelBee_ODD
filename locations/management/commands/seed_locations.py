from django.core.management.base import BaseCommand
from locations.models import Region, Department, Commune

class Command(BaseCommand):
    help = "Seed simple des régions/départements/communes (exemple)."

    def handle(self, *args, **options):
        # Exemple minimal. Remplace par tes vraies données.
        data = {
            "Littoral": {
                "Wouri": ["Douala I", "Douala II", "Douala III", "Douala IV", "Douala V"],
                "Sanaga-Maritime": ["Edéa I", "Edéa II"],
            },
            "Centre": {
                "Mfoundi": ["Yaoundé I", "Yaoundé II", "Yaoundé III"],
            },
        }

        for region_name, deps in data.items():
            region, _ = Region.objects.get_or_create(name=region_name)
            for dep_name, communes in deps.items():
                dep, _ = Department.objects.get_or_create(region=region, name=dep_name)
                for com_name in communes:
                    Commune.objects.get_or_create(department=dep, name=com_name)

        self.stdout.write(self.style.SUCCESS("Seed locations terminé ✅"))
