from django.db import models
from.MstVerifierField import MstVerifierField
from .BaseModel import BaseModel

class MstVerifierRules(BaseModel):
    verifier_field_id = models.ForeignKey(MstVerifierField, on_delete=models.CASCADE, related_name='verifier_fields', db_column='VERIFIER_FIELD_ID')
    design_doc = models.CharField(max_length=255, db_column='DESIGN_DOC')
    rule_number = models.CharField(max_length=50, unique=True, db_column='RULE_NUMBER')
    
    
    class Meta:
        db_table = 'MST_VERIFIER_RULES'
        verbose_name = 'Verifier Rules'
        verbose_name_plural = 'Verifier Rules'
    
    def __str__(self):
        return self.rule_number