from django.db import models
from .MstSubCategory import MstSubCategory
from .BaseModel import BaseModel

class PCBConditions(BaseModel):
    id = models.AutoField(primary_key=True, editable=False, db_column='ID')
    sub_category_id = models.ForeignKey(
        MstSubCategory, 
        on_delete=models.CASCADE,
        related_name='pcb_conditions',
        db_column='SUB_CATEGORY_ID'
    )
    
    # Field for the condition to be checked (e.g., pcb_size)
    condition_parameter = models.CharField(
        max_length=255,
        db_column='CONDITION_PARAMETER'
    )
    
    # Operator for comparison (>=, >, =, etc.)
    condition_operator = models.CharField(
        max_length=10,
        choices=[
            ('gte', 'Greater than or equal to'),
            ('gt', 'Greater than'),
            ('eq', 'Equal to'),
            ('lt', 'Less than'),
            ('lte', 'Less than or equal to'),
        ],
        db_column='CONDITION_OPERATOR'
    )
    
    # Value to compare against (e.g., 0.25, 0.80)
    condition_value = models.DecimalField(
        max_digits=4,
        decimal_places=4,
        db_column='CONDITION_VALUE'
    )
    
    # Parameter to be validated (e.g., dielectric_material_thickness)
    compared_parameter = models.CharField(
        max_length=255,
        db_column='COMPARED_PARAMETER'
    )
    
    # Minimum acceptable value
    min_value = models.DecimalField(
        max_digits=4,
        decimal_places=4,
        null=True,
        blank=True,
        db_column='MIN_VALUE'
    )
    
    # Maximum acceptable value
    max_value = models.DecimalField(
        max_digits=4,
        decimal_places=4,
        null=True,
        blank=True,
        db_column='MAX_VALUE'
    )
    



    class Meta:
        verbose_name = 'PCB Condition'
        verbose_name_plural = 'PCB Conditions'
        
        

    def __str__(self):
        return f"PCB Condition: {self.condition_parameter} {self.condition_operator} {self.condition_value}"
