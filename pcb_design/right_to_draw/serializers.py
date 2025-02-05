from rest_framework import serializers

from .models import MstComponent
from .authentication import CustomUser
from django.contrib.auth.password_validation import validate_password
from .models import CADDesignTemplates, CADVerifierTemplates,CADApproverTemplates
from masters.models import MstSubCategory,MstCategory, MstSectionRules, MstSectionGroupings,MstSubCategoryTwo,\
    MstVerifierField


class ComponentSerializer(serializers.ModelSerializer):

    class Meta:
        model = MstComponent
        fields = ['id', 'component_name', 'description']


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
        fields = ['id', 'design_doc', 'rule_number', 'parameter', 'min_value', 'max_value', 'nominal', 'comments']       


class CADDesignTemplatesSerializer(serializers.ModelSerializer):       
    class Meta:
        model = CADDesignTemplates
        fields = '__all__'

   

class SectionGroupingsSerializer(serializers.ModelSerializer):
    rules = SectionRulesSerializer(many=True)

    class Meta:
        model = MstSectionGroupings
        fields = ['id', 'design_doc', 'section_name', 'rules', 'design_options']
        

class SubCategoryTwoSerializer(serializers.ModelSerializer):    
    class Meta:
        model = MstSubCategoryTwo
        fields = ['id', 'sub_2_category_name']

       
class CustomSubCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(source="sub_category_name")
    is_design_options = serializers.BooleanField()
    is_sub_2_category = serializers.BooleanField()

    @staticmethod
    def from_model(sub_category):
        subcategory_relation = sub_category.subcategory.first()
        return {
            "id": sub_category.id,
            "name": sub_category.sub_category_name,
            "is_design_options": getattr(subcategory_relation, "is_design_options", False),
            "is_sub_2_category": getattr(subcategory_relation, "is_sub_2_category", False),
        }


class CustomCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(source="category_name")
    sub_categories = CustomSubCategorySerializer(many=True)

    @staticmethod
    def from_model(category):
        return {
            "id": category.id,
            "name": category.category_name,
            "sub_categories": [
                CustomSubCategorySerializer.from_model(sub_category)
                for sub_category in category.subcategories.all()
            ],
        }


class CustomComponentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(source="component_name")
    categories = CustomCategorySerializer(many=True)

    @staticmethod
    def from_model(component):
        return {
            "id": component.id,
            "name": component.component_name,
            "categories": [
                CustomCategorySerializer.from_model(category)
                for category in component.component_categories.all()
            ],
        }


class MstVerifierFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstVerifierField
        fields = ['id', 'field_name']


class CADVerifierTemplateSerializer(serializers.ModelSerializer):       
    class Meta:
        model = CADVerifierTemplates
        fields = '__all__'

class CADApproverTemplateSerializer(serializers.ModelSerializer):       
    class Meta:
        model = CADApproverTemplates
        fields = '__all__'
        
class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
  
    class Meta:
        model = CustomUser
        fields = ( 'password', 'password2', 'email')
    
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
    

    