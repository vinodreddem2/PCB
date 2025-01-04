import uuid
from django.db import models
from .MstCategory import MstCategory
from .BaseModel import BaseModel
class MstSubCategory(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sub_category_name = models.CharField(max_length=255)
    category_Id = models.ForeignKey(MstCategory, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.sub_category_name
