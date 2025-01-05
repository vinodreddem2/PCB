import uuid
from django.db import models
from .MstSubCategory import MstSubCategory
from .BaseModel import BaseModel


class MstSubCategoryRelations(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    sub_category_id = models.ForeignKey(MstSubCategory, on_delete=models.CASCADE, related_name='subcategory', unique=True)
    is_design_options = models.BooleanField(default=False)
    is_sub_2_category  = models.BooleanField(default=False)

    def __str__(self):
        return self.sub_category_id
