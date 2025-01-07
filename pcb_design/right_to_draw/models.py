from django.db import models
from masters.models.MstComponet import MstComponent
from masters.models.BaseModel import BaseModel


class CADDesignTemplates(BaseModel):
    opp_number = models.CharField(max_length=255, unique=True)
    opu_number = models.CharField(max_length=255, unique=True)
    edu_number = models.CharField(max_length=255, unique=True)
    model_name = models.CharField(max_length=255, unique=True)
    part_number = models.CharField(max_length=255, unique=True)
    revision_number = models.CharField(max_length=255, unique=True)
    component_Id = models.ForeignKey(MstComponent, on_delete=models.CASCADE, related_name='design_templates')
    pcb_specifications = models.JSONField()
    smt_design_options = models.JSONField()
    
    def __str__(self):
        return f"{self.model_name} ({self.part_number})"
