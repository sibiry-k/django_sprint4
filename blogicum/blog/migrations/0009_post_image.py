# Generated by Django 3.2.16 on 2023-10-29 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_remove_comment_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Фото'),
        ),
    ]
