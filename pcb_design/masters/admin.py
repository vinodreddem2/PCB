from django.contrib import admin
from .models import MstComponent, MstCategory, MstSubCategory, MstSectionRules, MstDesignOptions, MstSubCategoryRelations, MstSubCategoryTwo
# Register your models here.
admin.site.register((MstComponent, MstCategory, MstSubCategory, MstSectionRules, MstDesignOptions,MstSubCategoryRelations, MstSubCategoryTwo))