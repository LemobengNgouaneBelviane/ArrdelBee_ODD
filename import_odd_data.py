import csv
import re
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arrdel_backend.settings')
django.setup()

from odd.models import SDG, SDGTarget, SDGIndicator

def import_mvp_odds():
    csv_file = "../ODD, Objctifs, Cibles et Indicateurs 082023(1).csv"
    
    # Priority ODDs for MVP
    # Based on docs: 3, 4, 6, 9, 11 + added 1 to make it 6
    MVP_ODD_NUMBERS = [1, 3, 4, 6, 9, 11]
    
    ODD_COLORS = {
        1: "#E5243B",
        3: "#4C9F38",
        4: "#C5192D",
        6: "#26BDE2",
        9: "#FD6925",
        11: "#FB9D24"
    }

    print(f"Starting import from {csv_file}...")

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        current_odd = None
        current_target = None
        
        for row in reader:
            if not row or not row[0].strip():
                continue
            
            line = row[0].strip().strip('"').strip()
            
            # Match ODD Objective: "Objectif 1. ..."
            obj_match = re.match(r'^Objectif\s+(\d+)\.\s+(.+)$', line)
            if obj_match:
                odd_num = int(obj_match.group(1))
                if odd_num in MVP_ODD_NUMBERS:
                    name = obj_match.group(2)
                    current_odd, created = SDG.objects.get_or_create(
                        number=odd_num,
                        defaults={'name': name, 'color': ODD_COLORS.get(odd_num, "#000000")}
                    )
                    if not created:
                        current_odd.name = name
                        current_odd.save()
                    print(f"Importing ODD {odd_num}: {name}")
                else:
                    current_odd = None
                current_target = None
                continue
            
            if not current_odd:
                continue

            # Match Indicator first to avoid catching targets incorrectly
            indicator_match = re.match(r'^(\d+\.[0-9a-z]+(?:\.[0-9a-z]+)+)(?:\s+|-|)(.*)$', line, re.IGNORECASE)
            if indicator_match:
                if not current_target:
                    continue
                code = indicator_match.group(1).lower()
                desc = indicator_match.group(2).strip()
                indicator, created = SDGIndicator.objects.get_or_create(
                    code=code,
                    defaults={'target': current_target, 'description': desc}
                )
                if not created:
                    indicator.description = desc
                    indicator.save()
                continue
            
            # Match Target
            target_match = re.match(r'^(\d+\.[0-9a-z]+)(?:\s+|-|)(.*)$', line, re.IGNORECASE)
            if target_match:
                code = target_match.group(1).lower()
                desc = target_match.group(2).strip()
                current_target, created = SDGTarget.objects.get_or_create(
                    code=code,
                    defaults={'sdg': current_odd, 'description': desc}
                )
                if not created:
                    current_target.description = desc
                    current_target.save()
                continue

    print("Import completed successfully!")

if __name__ == "__main__":
    import_mvp_odds()
