from rest_framework import serializers
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from .models import MstComponent
from .models import CADDesignTemplates
from masters.models import MstSubCategory,MstCategory, MstSectionRules, MstSectionGroupings,MstSubCategoryTwo
from authentication.models import CustomUser
from .utils import token_generator
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


class CADDesignTemplatesSerializer(serializers.ModelSerializer):
    component_Id = ComponentSerializer()  # Nested serializer

    class Meta:
        model = CADDesignTemplates
        fields = '__all__'        


class SectionGroupingsSerializer(serializers.ModelSerializer):
    rules = SectionRulesSerializer(many=True)

    class Meta:
        model = MstSectionGroupings
        fields = ['id', 'design_doc', 'design_name', 'rules']
        

class SubCategoryTwoSerializer(serializers.ModelSerializer):
    sub_category_id = SubCategorySerializer()  # Nested serializer for SubCategory

    class Meta:
        model = MstSubCategoryTwo
        fields = ['id', 'sub_2_category_name', 'sub_category_id']

       
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


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
            return value
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, min_length=8)
    token = serializers.CharField()
    uidb64 = serializers.CharField()

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data['uidb64']))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError("Invalid reset link")

        if not token_generator.check_token(user, data['token']):
            raise serializers.ValidationError("Reset link has expired")

        return data