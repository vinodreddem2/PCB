from django.db import models
from .MstComponet import MstComponent
from .BaseModel import BaseModel


class MstCategory(BaseModel):
    id = models.AutoField(primary_key=True,editable=False)
    category_name = models.CharField(max_length=255)
    component_Id = models.ForeignKey(MstComponent, on_delete=models.CASCADE, related_name='component_categories')
    
    class Meta:
        unique_together = ('category_name', 'component_Id')  

    def __str__(self):
        return self.category_name
