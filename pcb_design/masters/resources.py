from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import MstComponent, MstCategory, MstSubCategory, MstSubCategoryTwo, MstDesignOptions, \
    MstSectionRules, MstSectionGroupings
from django.utils import timezone
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from django.core.exceptions import ObjectDoesNotExist


class CustomForeignKeyWidget(ForeignKeyWidget):
    def __init__(self, model, field='id'):        
        super().__init__(model, field)
    
    def clean(self, value, row=None, *args, **kwargs):
        if value:            
            try:
                response =  super().clean(value, row, *args, **kwargs)
                return response
            except ObjectDoesNotExist as e:                
                try:
                    value = int(value)
                    res = self.model.objects.get(**{'id': value})               
                    return res
                except ObjectDoesNotExist:
                    raise ValueError(f"{self.model.__name__} with {self.field}={value} does not exist.")
        return None

class CustomManyToManyWidget(ManyToManyWidget):
    def __init__(self, model, separator=None, field=None, **kwargs):        
        if separator is None:
            separator = ","
        if field is None:
            field = "id"
        self.model = model
        self.separator = separator
        self.field = field
        super().__init__(self.model, self.separator, self.field, **kwargs)

    def clean(self, value, row=None, **kwargs):        
        if not value:
            return self.model.objects.none()        
        if isinstance(value, (float, int)):
            ids = [int(value)]
        else:
            ids = value.split(self.separator)
            # This Needs to change If you change Primary Key from AutoField to Other Field
            ids = filter(None, [int(i.strip()) for i in ids])            
        res = self.model.objects.filter(**{"%s__in" % self.field: ids})        
        return res


def before_save_instance_update_create_date(instance, model):
    try:
        existing_instance = model.objects.get(pk=instance.pk)
        instance.created_at = existing_instance.created_at if \
            existing_instance.created_at else timezone.now()
    except Exception as ex:
        instance.created_at = timezone.now()
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
    
    def before_save_instance(self, instance, row, using_transactions, dry_run, **kwargs):        
        if instance:
            if not instance.created_at:
                instance = before_save_instance_update_create_date(instance, MstComponent)


class MstCategoryResource(resources.ModelResource):    
    component_Id = fields.Field(
        column_name='component_Id',
        attribute='component_Id',
        widget=CustomForeignKeyWidget(MstComponent, field='component_name')
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
    
    def before_save_instance(self, instance, row, using_transactions, dry_run, **kwargs):        
        if instance:
            if not instance.created_at:
                print()
                instance = before_save_instance_update_create_date(instance, MstCategory)


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
                print()
                instance = before_save_instance_update_create_date(instance, MstSubCategory)



class MstSubCategoryTwoResource(resources.ModelResource):    
    sub_category_id = fields.Field(
        column_name='sub_category_id',
        attribute='sub_category_id',
        widget=ForeignKeyWidget(MstSubCategory, field='id')
    )

    class Meta:
        model = MstSubCategoryTwo
        fields = ('id', 'sub_2_category_name', 'sub_category_id')
        import_id_fields = ('sub_2_category_name', 'sub_category_id') 
        primary_key = 'id'
        skip_unchanged = True
        report_skipped = False
        sheet_name = "SubCategoryTwos"
        update_on_import = True
    
    def before_save_instance(self, instance, row, using_transactions, dry_run, **kwargs):        
        if instance:
            if not instance.created_at:
                print()
                instance = before_save_instance_update_create_date(instance, MstSubCategoryTwo)


class MstDesignOptionsResource(resources.ModelResource):    
    sub_category_id = fields.Field(
        column_name='sub_category_id',
        attribute='sub_category_id',
        widget=ForeignKeyWidget(MstSubCategory, field='id')
    )

    class Meta:
        model = MstDesignOptions
        fields = ('id', 'desing_option_name', 'sub_category_id')
        import_id_fields = ('desing_option_name', 'sub_category_id') 
        primary_key = 'id'
        skip_unchanged = True
        report_skipped = False
        sheet_name = "DesignOptions"
        update_on_import = True
    
    def before_save_instance(self, instance, row, using_transactions, dry_run, **kwargs):        
        if instance:
            if not instance.created_at:
                print()
                instance = before_save_instance_update_create_date(instance, MstDesignOptions)


class MstSectionRulesResource(resources.ModelResource):
    class Meta:
        model = MstSectionRules
        fields = ('id', 'design_doc', 'rule_number', 'parameter', 'min_value', 'max_value', 'nominal', 'comments')
        import_id_fields = ('rule_number', 'design_doc')
        primary_key = 'id'
        skip_unchanged = True
        report_skipped = False
        sheet_name = "SectionRules"
        update_on_import = True

    def before_save_instance(self, instance, row, using_transactions, dry_run, **kwargs):
        if instance:            
            if not instance.created_at:
                instance = before_save_instance_update_create_date(instance, MstSectionRules)


class MstSectionGroupingsResource(resources.ModelResource):
    rules = fields.Field(
        column_name='rules',
        attribute='rules',        
        widget=CustomManyToManyWidget(MstSectionRules, field='id', separator=',')
    )
    design_options = fields.Field(
        column_name='design_options',
        attribute='design_options',
        widget=CustomManyToManyWidget(MstDesignOptions, field='id',  separator=',')
    )

    class Meta:
        model = MstSectionGroupings
        fields = ('id', 'design_doc', 'section_name', 'rules', 'design_options')
        import_id_fields = ('design_doc', 'section_name')
        primary_key = 'id'
        skip_unchanged = True
        report_skipped = False
        sheet_name = "SectionGroupings"
        update_on_import = True

    def before_save_instance(self, instance, row, using_transactions, dry_run, **kwargs):
        """
        This method is used to modify instances before they are saved to the database.
        You can add any custom logic here, such as setting timestamps or modifying fields before saving.
        """
        if instance:
            if not instance.created_at:
                instance = before_save_instance_update_create_date(instance, MstSectionGroupings)