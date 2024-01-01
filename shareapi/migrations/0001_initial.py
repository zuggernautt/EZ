# Generated by Django 5.0 on 2024-01-01 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='files/')),
                ('file_type', models.CharField(max_length=10)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
