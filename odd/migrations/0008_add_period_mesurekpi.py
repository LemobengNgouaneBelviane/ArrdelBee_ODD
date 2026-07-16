from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('odd', '0007_add_preuve'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('quarter', models.IntegerField(
                    choices=[(1, 'T1'), (2, 'T2'), (3, 'T3'), (4, 'T4')],
                    null=True, blank=True,
                )),
                ('is_closed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-year', '-quarter']},
        ),
        migrations.AddConstraint(
            model_name='period',
            constraint=models.UniqueConstraint(fields=['year', 'quarter'], name='unique_year_quarter'),
        ),
        migrations.CreateModel(
            name='MesureKPI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valeur',       models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)),
                ('valeur_cible', models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)),
                ('statut', models.CharField(
                    max_length=10,
                    choices=[('draft','Brouillon'),('submitted','Soumis'),('validated','Validé'),('rejected','Rejeté')],
                    default='draft',
                )),
                ('commentaire', models.TextField(blank=True, default='')),
                ('date_saisie', models.DateTimeField(auto_now_add=True)),
                ('updated_at',  models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='mesures_kpi', to='odd.project',
                )),
                ('indicator', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='mesures', to='odd.sdgindicator',
                )),
                ('period', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='mesures', to='odd.period',
                )),
                ('saisi_par', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='mesures_saisies', to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={'ordering': ['-date_saisie']},
        ),
        migrations.AddConstraint(
            model_name='mesurekpi',
            constraint=models.UniqueConstraint(
                fields=['project', 'indicator', 'period'],
                name='unique_project_indicator_period',
            ),
        ),
    ]
