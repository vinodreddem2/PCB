import uuid
from django.db import models
from .MstSubCategory import MstSubCategory
from .MstSectionRules import MstSectionRules
from .BaseModel import BaseModel


class MstDesignOptions(BaseModel):
    id = models.AutoField(primary_key=True,editable=False)
    design_option_name = models.CharField(max_length=255, unique=True)
    Rules = models.ManyToManyField(MstSectionRules)
    SubCategories = models.ManyToManyField(MstSubCategory)    

    def __str__(self):
        return self.design_option_name
