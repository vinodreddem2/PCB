from django.db import models

from authentication.models import CustomUser
class BaseModel(models.Model):
    created_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='%(class)s_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='%(class)s_updated_by')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

