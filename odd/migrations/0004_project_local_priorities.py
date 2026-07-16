from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odd', '0003_remove_projectworkflowtrace_actor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='local_priorities',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
