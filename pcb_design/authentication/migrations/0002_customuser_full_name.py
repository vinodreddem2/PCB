# Generated by Django 5.0.10 on 2025-01-31 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(default='Test User', max_length=255),
            preserve_default=False,
        ),
    ]
