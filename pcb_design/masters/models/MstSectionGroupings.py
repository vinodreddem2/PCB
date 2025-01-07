from django.db import models

from .BaseModel import BaseModel
from .MstSubCategory import MstSubCategory
from .MstSectionRules import MstSectionRules


class MstSectionGroupings(BaseModel):
    id = models.AutoField(primary_key=True,editable=False)
    design_doc = models.CharField(max_length=255)
    design_name = models.CharField(max_length=255, unique=True)
    rules = models.ManyToManyField(MstSectionRules)
    sub_categories = models.ManyToManyField(MstSubCategory)    

    class Meta:
        verbose_name = 'Section Grouping'
        verbose_name_plural = 'Section Groupings'
    def __str__(self):
        return f"{self.design_name}-{self.design_doc}"
