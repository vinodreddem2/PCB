from django.db import models

from .BaseModel import BaseModel


class MstSectionRules(BaseModel):
    id = models.AutoField(primary_key=True,editable=False)
    design_doc = models.CharField(max_length=255)
    rule_number = models.CharField(max_length=50, unique=True)
    parameter = models.CharField(max_length=255)
    min_value = models.FloatField()
    max_value = models.FloatField()
    nominal = models.FloatField()
    comments = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Section Rule'
        verbose_name_plural = 'Section Rules' 
    def __str__(self):
        return f"Rule {self.rule_number}"
