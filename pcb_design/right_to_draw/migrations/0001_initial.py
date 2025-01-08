# Generated by Django 5.0.10 on 2025-01-08 12:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('masters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CADDesignTemplates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opp_number', models.CharField(db_column='OPP_NUMBER', max_length=255, unique=True)),
                ('opu_number', models.CharField(db_column='OPU_NUMBER', max_length=255, unique=True)),
                ('edu_number', models.CharField(db_column='EDU_NUMBER', max_length=255, unique=True)),
                ('model_name', models.CharField(db_column='MODEL_NAME', max_length=255, unique=True)),
                ('part_number', models.CharField(db_column='PART_NUMBER', max_length=255, unique=True)),
                ('revision_number', models.CharField(db_column='REVISION_NUMBER', max_length=255, unique=True)),
                ('pcb_specifications', models.JSONField(db_column='PCB_SPECIFICATIONS')),
                ('smt_design_options', models.JSONField(db_column='SMT_DESIGN_OPTIONS')),
                ('component_Id', models.ForeignKey(db_column='COMPONENT_ID', on_delete=django.db.models.deletion.CASCADE, related_name='design_templates', to='masters.mstcomponent')),
            ],
        ),
    ]
