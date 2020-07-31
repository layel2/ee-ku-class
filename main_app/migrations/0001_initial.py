# Generated by Django 3.0.3 on 2020-04-21 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='class_dt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_day', models.CharField(max_length=255)),
                ('dt_time', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='lecturer',
            fields=[
                ('lecturer_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('lecturer_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='semester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('term', models.IntegerField(choices=[(1, 'First'), (2, 'Second'), (3, 'Summer')])),
            ],
        ),
        migrations.CreateModel(
            name='sub_list',
            fields=[
                ('sub_id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_code', models.CharField(max_length=255)),
                ('sub_name', models.CharField(max_length=255)),
                ('sub_credit', models.IntegerField()),
                ('sub_year', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='sub_sec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=255)),
                ('sec_room', models.CharField(max_length=255)),
                ('sec_amount', models.IntegerField()),
                ('sec_student_type', models.CharField(max_length=255)),
                ('dt_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.class_dt')),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.lecturer')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.semester')),
                ('sub_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.sub_list')),
            ],
        ),
    ]