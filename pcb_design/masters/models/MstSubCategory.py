from django.db import models

from .MstCategory import MstCategory
from .BaseModel import BaseModel


class MstSubCategory(BaseModel):
    id = models.AutoField(primary_key=True,editable=False)
    sub_category_name = models.CharField(max_length=255)
    category_Id = models.ForeignKey(MstCategory, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        unique_together = ('sub_category_name', 'category_Id') 
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub Categories' 

    def __str__(self):
        return f"{self.sub_category_name} ({self.category_Id.category_name})"

