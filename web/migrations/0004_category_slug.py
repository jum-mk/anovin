# Generated by Django 4.1.4 on 2022-12-20 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_subscriber'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.CharField(default='', max_length=120),
            preserve_default=False,
        ),
    ]