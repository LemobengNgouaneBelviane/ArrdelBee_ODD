import os
import django
import pandas as pd

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arrdel_backend.settings')
django.setup()

from odd.models import Project
from accounts.models import User

def import_projects():
    # Use the full name found in list_dir
    file_path = "../Liste des tableaux des Cadres logiques 19082024 Ok.xlsx"
    print(f"Checking for file: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        # Try local case just in case
        file_path = "Liste des tableaux des Cadres logiques 19082024 Ok.xlsx"
        if not os.path.exists(file_path):
            print(f"File still not found: {file_path}")
            return

    # Use first superuser
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = User.objects.first()
    
    if not admin_user:
        print("No user found. Run create_admin.py first.")
        return
    
    print(f"Using user: {admin_user.email}")

    print("Reading Excel file...")
    try:
        # Optimization: use usecols if possible, but let's just read first rows to avoid hang
        df = pd.read_excel(file_path, sheet_name=0, nrows=200)
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return
        
    print(f"Found {len(df)} rows in first sheet.")
    
    projects_added = 0
    # Clean up old data for demo if needed? No, let's just append.
    
    # Heuristics for finding projects:
    # Based on peek, columns 4 and 5 had text like "Aménagement de 5km..."
    # Columns: 0: Index, 1: NaN, 2: Index, 3: Location, 4: Activity 1, 5: Activity 2...
    
    for index, row in df.iterrows():
        # Look at columns 4, 5, 6
        for col_idx in [4, 5, 6]:
            if col_idx >= len(row): continue
            
            val = str(row.iloc[col_idx]).strip()
            if len(val) > 15 and val.lower() != 'nan' and 'page' not in val.lower():
                name = val[:255]
                territory = str(row.iloc[3]).strip() if len(row) > 3 else "Cameroun"
                if territory.lower() == 'nan': territory = "Cameroun"
                
                if not Project.objects.filter(name=name).exists():
                    Project.objects.create(
                        name=name,
                        description=val,
                        territory=territory,
                        owner=admin_user,
                        status='active'
                    )
                    projects_added += 1
                    print(f"  + Added: {name[:50]}...")
                    if projects_added >= 20: 
                        break
        if projects_added >= 20:
            break

    print(f"\n✅ Successfully imported {projects_added} projects into the database.")

if __name__ == "__main__":
    import_projects()
