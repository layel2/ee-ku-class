# Generated by Django 3.0.3 on 2020-05-01 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sub_sec',
            name='sec_room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.room'),
        ),
    ]
