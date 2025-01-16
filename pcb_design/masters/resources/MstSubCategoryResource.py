from import_export import resources, fields
from models import MstCategory, MstSubCategory
from .utility import before_save_instance_update_create_date, CustomForeignKeyWidget


class MstSubCategoryResource(resources.ModelResource):    
    category_Id = fields.Field(
        column_name='category_Id',
        attribute='category_Id',
        widget=CustomForeignKeyWidget(MstCategory, field='category_name')
    )

    class Meta:
        model = MstSubCategory
        fields = ('id', 'sub_category_name', 'category_Id')
        import_id_fields = ('sub_category_name', 'category_Id') 
        primary_key = 'id'
        skip_unchanged = True
        report_skipped = False
        sheet_name = "SubCategories"
        update_on_import = True
    
    def before_save_instance(self, instance, row, using_transactions, dry_run, **kwargs):        
        if instance:
            if not instance.created_at:                
                instance = before_save_instance_update_create_date(instance, MstSubCategory)
