# Generated by Django 3.2.16 on 2023-10-28 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_comment_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='is_published',
        ),
    ]
