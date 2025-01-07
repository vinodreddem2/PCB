# Generated by Django 5.0.10 on 2025-01-07 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mstcategory',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='mstcomponent',
            options={'verbose_name': 'Component', 'verbose_name_plural': 'Components'},
        ),
        migrations.AlterModelOptions(
            name='mstsectiongroupings',
            options={'verbose_name': 'Section Grouping', 'verbose_name_plural': 'Section Groupings'},
        ),
        migrations.AlterModelOptions(
            name='mstsectionrules',
            options={'verbose_name': 'Section Rule', 'verbose_name_plural': 'Section Rules'},
        ),
        migrations.AlterModelOptions(
            name='mstsubcategory',
            options={'verbose_name': 'Sub Category', 'verbose_name_plural': 'Sub Categories'},
        ),
        migrations.AlterModelOptions(
            name='mstsubcategorytwo',
            options={'verbose_name': 'Sub Category Two', 'verbose_name_plural': 'Sub Category Twos'},
        ),
    ]
