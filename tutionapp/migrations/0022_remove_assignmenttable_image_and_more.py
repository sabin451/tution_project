# Generated by Django 4.2.5 on 2023-10-27 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutionapp', '0021_remove_assignmenttable_file_assignmenttable_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmenttable',
            name='image',
        ),
        migrations.AddField(
            model_name='assignmenttable',
            name='pdf_file',
            field=models.FileField(null=True, upload_to='pdfs/'),
        ),
    ]
