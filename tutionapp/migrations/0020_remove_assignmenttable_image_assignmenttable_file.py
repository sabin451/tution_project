# Generated by Django 4.2.4 on 2023-10-25 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutionapp', '0019_assignmenttable_courseid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmenttable',
            name='image',
        ),
        migrations.AddField(
            model_name='assignmenttable',
            name='file',
            field=models.FileField(null=True, upload_to='assignments/'),
        ),
    ]
