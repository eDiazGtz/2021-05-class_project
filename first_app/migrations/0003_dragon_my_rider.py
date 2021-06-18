# Generated by Django 2.2 on 2021-05-28 00:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_rider'),
    ]

    operations = [
        migrations.AddField(
            model_name='dragon',
            name='my_rider',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='my_dragons', to='first_app.Rider'),
            preserve_default=False,
        ),
    ]