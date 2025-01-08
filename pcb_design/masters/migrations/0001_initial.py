# Generated by Django 5.0.10 on 2025-01-08 12:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MstComponent',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='UPDATED_AT')),
                ('id', models.AutoField(db_column='ID', editable=False, primary_key=True, serialize=False)),
                ('component_name', models.CharField(db_column='COMPONENT_NAME', max_length=255, unique=True)),
                ('description', models.CharField(blank=True, db_column='DESCRIPTION', max_length=255, null=True)),
                ('created_by', models.ForeignKey(blank=True, db_column='CREATED_BY', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, db_column='UPDATED_BY', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Component',
                'verbose_name_plural': 'Components',
            },
        ),
        migrations.CreateModel(
            name='MstCategory',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='UPDATED_AT')),
                ('id', models.AutoField(db_column='ID', editable=False, primary_key=True, serialize=False)),
                ('category_name', models.CharField(db_column='CATEGORY_NAME', max_length=255)),
                ('created_by', models.ForeignKey(blank=True, db_column='CREATED_BY', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, db_column='UPDATED_BY', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
                ('component_Id', models.ForeignKey(db_column='COMPONENT_ID', on_delete=django.db.models.deletion.CASCADE, related_name='component_categories', to='masters.mstcomponent')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'unique_together': {('category_name', 'component_Id')},
            },
        ),
        migrations.CreateModel(
            name='MstSectionRules',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='UPDATED_AT')),
                ('id', models.AutoField(db_column='ID', editable=False, primary_key=True, serialize=False)),
                ('design_doc', models.CharField(db_column='DESIGN_DOC', max_length=255)),
                ('rule_number', models.CharField(db_column='RULE_NUMBER', max_length=50, unique=True)),
                ('parameter', models.CharField(db_column='PARAMETER', max_length=255)),
                ('min_value', models.CharField(blank=True, db_column='MIN_VALUE', max_length=10, null=True)),
                ('max_value', models.CharField(blank=True, db_column='MAX_VALUE', max_length=10, null=True)),
                ('nominal', models.CharField(blank=True, db_column='NOMINAL', max_length=10, null=True)),
                ('comments', models.TextField(blank=True, db_column='COMMENTS', null=True)),
                ('created_by', models.ForeignKey(blank=True, db_column='CREATED_BY', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, db_column='UPDATED_BY', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Section Rule',
                'verbose_name_plural': 'Section Rules',
            },
        ),
        migrations.CreateModel(
            name='MstSubCategory',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='UPDATED_AT')),
                ('id', models.AutoField(db_column='ID', editable=False, primary_key=True, serialize=False)),
                ('sub_category_name', models.CharField(db_column='SUB_CATEGORY_NAME', max_length=255)),
                ('category_Id', models.ForeignKey(db_column='CATEGORY_ID', on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='masters.mstcategory')),
                ('created_by', models.ForeignKey(blank=True, db_column='CREATED_BY', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, db_column='UPDATED_BY', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sub Category',
                'verbose_name_plural': 'Sub Categories',
                'unique_together': {('sub_category_name', 'category_Id')},
            },
        ),
        migrations.CreateModel(
            name='MstSectionGroupings',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='UPDATED_AT')),
                ('id', models.AutoField(db_column='ID', editable=False, primary_key=True, serialize=False)),
                ('design_doc', models.CharField(db_column='DESIGN_DOC', max_length=255)),
                ('design_name', models.CharField(db_column='DESIGN_NAME', max_length=255, unique=True)),
                ('created_by', models.ForeignKey(blank=True, db_column='CREATED_BY', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, db_column='UPDATED_BY', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
                ('rules', models.ManyToManyField(db_column='RULES', to='masters.mstsectionrules')),
                ('sub_categories', models.ManyToManyField(db_column='SUB_CATEGORIES', to='masters.mstsubcategory')),
            ],
            options={
                'verbose_name': 'Section Grouping',
                'verbose_name_plural': 'Section Groupings',
            },
        ),
        migrations.CreateModel(
            name='MstSubCategoryTwo',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='UPDATED_AT')),
                ('id', models.AutoField(db_column='ID', editable=False, primary_key=True, serialize=False)),
                ('sub_2_category_name', models.CharField(db_column='SUB_2_CATEGORY_NAME', max_length=255)),
                ('created_by', models.ForeignKey(blank=True, db_column='CREATED_BY', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('sub_category_id', models.ForeignKey(db_column='SUB_CATEGORY_ID', on_delete=django.db.models.deletion.CASCADE, related_name='subcategories2', to='masters.mstsubcategory')),
                ('updated_by', models.ForeignKey(blank=True, db_column='UPDATED_BY', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sub Category Two',
                'verbose_name_plural': 'Sub Category Twos',
                'unique_together': {('sub_2_category_name', 'sub_category_id')},
            },
        ),
    ]
