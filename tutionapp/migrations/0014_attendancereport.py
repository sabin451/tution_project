# Generated by Django 4.2.4 on 2023-10-17 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutionapp', '0013_teacherattendancetable'),
    ]

    operations = [
        migrations.CreateModel(
            name='attendancereport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(null=True)),
                ('date', models.DateField()),
                ('userid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
