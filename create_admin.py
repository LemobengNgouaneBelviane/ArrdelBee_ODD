#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arrdel_backend.settings')
django.setup()

from accounts.models import User

# Create admin user if not exists
if not User.objects.filter(email='admin@test.com').exists():
    User.objects.create_superuser(
        email='admin@test.com',
        full_name='Admin User',
        password='admin123'
    )
    print("✅ Admin user created: admin@test.com / admin123")
else:
    print("⚠️  Admin user already exists")

# List all users
users = User.objects.all()
print(f"\n📋 Total users: {users.count()}")
for user in users:
    print(f"  - {user.email} (superuser: {user.is_superuser})")
