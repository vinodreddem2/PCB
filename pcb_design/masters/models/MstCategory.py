from django.db import models
from .MstComponet import MstComponent
from .BaseModel import BaseModel
import uuid
class MstCategory(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=255)
    component_Id = models.ForeignKey(MstComponent, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.category_name
