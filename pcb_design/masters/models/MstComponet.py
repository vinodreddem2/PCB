from django.db import models
from .BaseModel import BaseModel
import uuid
class MstComponent(BaseModel):

    component_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    component_name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.component_name