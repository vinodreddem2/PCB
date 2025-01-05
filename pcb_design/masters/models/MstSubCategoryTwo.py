import uuid
from django.db import models
from .MstSubCategory import MstSubCategory
from .BaseModel import BaseModel


class MstSubCategoryTwo(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sub_2_category_name = models.CharField(max_length=255)
    sub_category_id = models.ForeignKey(MstSubCategory, on_delete=models.CASCADE, related_name='subcategories2')

    class Meta:
        unique_together = ('sub_2_category_name', 'sub_category_id')

    def __str__(self):
        return self.sub_2_category_name
