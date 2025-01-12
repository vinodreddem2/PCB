from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import MstComponent, MstCategory
from django.utils import timezone


def before_save_instance_update_create_date(instance, model):
    try:
        existing_instance = model.objects.get(pk=instance.pk)
        instance.created_date = existing_instance.created_date if \
            existing_instance.created_date else timezone.now()
    except Exception as ex:
        instance.created_date = timezone.now()
    return instance


class MstComponentResource(resources.ModelResource):    
    class Meta:
        model = MstComponent
        fields = ('id', 'component_name', 'description')
        import_id_fields = ('component_name',)
        primary_key = 'id'
        skip_unchanged = True
        report_skipped = False
        sheet_name = "Components"
        update_on_import = True
    
    def before_save_instance(self, instance, using_transactions, dry_run):
        if not instance.created_date:
            instance = before_save_instance_update_create_date(instance, MstComponent)


class MstCategoryResource(resources.ModelResource):    
    component_Id = fields.Field(
        column_name='component_Id',
        attribute='component_Id',
        widget=ForeignKeyWidget(MstComponent, field='id')
    )

    class Meta:
        model = MstCategory
        fields = ('id', 'category_name', 'component_Id')
        import_id_fields = ('category_name', 'component_Id') 
        primary_key = 'id'
        skip_unchanged = True
        report_skipped = False
        sheet_name = "Categories"
        update_on_import = True
    
    def before_save_instance(self, instance, using_transactions, dry_run):
        if not instance.created_date:
            instance = before_save_instance_update_create_date(instance, MstCategory)