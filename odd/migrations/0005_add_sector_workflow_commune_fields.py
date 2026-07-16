import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odd', '0004_project_local_priorities'),
        ('locations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # ── 1. Modèle Sector ──
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, default='')),
            ],
            options={'ordering': ['name']},
        ),

        # ── 2. Nouveaux champs sur Project ──
        migrations.AddField(
            model_name='project',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='beneficiaries_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='rejection_reason',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='project',
            name='commune',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='odd_projects',
                to='locations.commune',
            ),
        ),
        migrations.AddField(
            model_name='project',
            name='sector',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='projects',
                to='odd.sector',
            ),
        ),

        # ── 3. Remettre les bons STATUS_CHOICES ──
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(
                choices=[
                    ('draft',              'Brouillon'),
                    ('submitted',          'Soumis'),
                    ('controlling_ctd',    'En contrôle CTD'),
                    ('validated_ctd',      'Validé CTD'),
                    ('controlling_arrdel', 'En contrôle ARRDEL'),
                    ('validated',          'Validé'),
                    ('rejected',           'Rejeté'),
                ],
                default='draft',
                max_length=20,
            ),
        ),

        # ── 4. Journal de workflow ──
        migrations.CreateModel(
            name='ProjectWorkflowTrace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_status', models.CharField(max_length=30)),
                ('to_status', models.CharField(max_length=30)),
                ('comment', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('actor', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='odd_workflow_actions',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('project', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='workflow_history',
                    to='odd.project',
                )),
            ],
            options={'ordering': ['-created_at']},
        ),

        # ── 5. Données initiales des secteurs ──
        migrations.RunSQL(
            sql="""
                INSERT INTO odd_sector (name, description) VALUES
                ('Santé',                 'Projets de construction, équipement et fonctionnement des structures sanitaires'),
                ('Eau et Assainissement', 'Adduction d''eau potable, drainage, gestion des déchets et assainissement'),
                ('Éducation',             'Construction et équipement des établissements scolaires et universitaires'),
                ('Infrastructure',        'Routes, ponts, bâtiments publics et aménagements urbains'),
                ('Énergie',               'Électrification, énergies renouvelables et économies d''énergie'),
                ('Développement Économique', 'Marchés, agriculture, artisanat, PME et économie locale'),
                ('Environnement',         'Protection de la nature, reboisement et gestion des ressources naturelles'),
                ('Gouvernance',           'Renforcement institutionnel, état civil, sécurité et administration locale');
            """,
            reverse_sql="DELETE FROM odd_sector;",
        ),
    ]
