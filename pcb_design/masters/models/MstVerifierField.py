from django.db import models
from .MstComponet import MstComponent
from .MstCategory import MstCategory
from .MstSubCategory import MstSubCategory
from .BaseModel import BaseModel


class MstVerifierField(BaseModel):
    
    id = models.AutoField(primary_key=True, editable=False, db_column='ID')
    component_Id = models.ForeignKey(MstComponent, on_delete=models.CASCADE,
                                     related_name='component_verifier_fields', db_column='COMPONENT_ID')
    category_Id = models.ForeignKey(MstCategory, on_delete=models.CASCADE,
                                        related_name='category_verifier_fields', db_column='CATEGORY_ID')
    sub_category_id = models.ManyToManyField(MstSubCategory,
                                        related_name='subcategory_verifier_fields', db_column='SUB_CATEGORY_ID')
    field_name = models.CharField(max_length=255, unique=True, db_column='FIELD_NAME')
    
    
    class Meta:
        db_table = 'MST_VERIFIER_FIELD'
        verbose_name = 'Verifier Field'
        verbose_name_plural = 'Verifier Fields'

    def __str__(self):
        return self.field_name