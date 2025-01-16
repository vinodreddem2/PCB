from django.db import models

from .MstComponet import MstComponent
from .MstCategory import MstCategory
from .MstSubCategory import MstSubCategory
from .BaseModel import BaseModel
from authentication.alias import AliasField


class MstConditions(BaseModel):
    id = models.AutoField(primary_key=True, editable=False, db_column='ID')
    subcategory = models.ForeignKey(MstSubCategory, on_delete=models.CASCADE, db_column='SUB_CATEGORY_ID')
    condition_variable = models.CharField(max_length=255, db_column='CONDITION_VARIABLE')
    condition_operator = models.CharField(max_length=2, db_column='CONDITION_OPERATOR', null=True, blank=True)
    condition_min_value = models.DecimalField(max_digits=10, decimal_places=2, db_column='CONDITION_MIN_VALUE', null=True, blank=True)
    condition_max_value = models.DecimalField(max_digits=10, decimal_places=2, db_column='CONDITION_MAX_VALUE', null=True, blank=True)
    comparison_variable = models.CharField(max_length=255, db_column='COMPARISON_VARIABLE')
    comparison_min_value = models.DecimalField(max_digits=10, decimal_places=2, db_column='COMPARISON_MIN_VALUE', null=True, blank=True)
    comparison_max_value = models.DecimalField(max_digits=10, decimal_places=2, db_column='COMPARISON_MAX_VALUE', null=True, blank=True)
    comparison_operator = models.CharField(max_length=20, db_column='COMPARISON_OPERATOR', null=True, blank=True)

    def __str__(self):
        return f"Condition for {self.category.name} - {self.condition_variable}"

