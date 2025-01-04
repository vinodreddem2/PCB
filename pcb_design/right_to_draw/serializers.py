from .models import MstComponent
from rest_framework import serializers
from masters.models import MstSubCategory,MstCategory, MstSectionRules, MstDesignOptions
from .models import CADDesignTemplates
class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstComponent
        fields = '__all__'
class CategorySerializer(serializers.ModelSerializer):
    component_Id = ComponentSerializer()  # Nested serializer
    class Meta:
        model = MstCategory
        fields = '__all__'
class SubCategorySerializer(serializers.ModelSerializer):
    category_Id = CategorySerializer()  # Nested serializer

    class Meta:
        model = MstSubCategory
        fields = '__all__'
class SectionRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstSectionRules
        fields = '__all__'        
class DesignOptionsSerializer(serializers.ModelSerializer):
    Rules = SectionRulesSerializer(many=True)
    SubCategories = SubCategorySerializer(many=True)

    class Meta:
        model = MstDesignOptions
        fields = '__all__'
class CADDesignTemplatesSerializer(serializers.ModelSerializer):
    component_Id = ComponentSerializer()  # Nested serializer

    class Meta:
        model = CADDesignTemplates
        fields = '__all__'
        
        
