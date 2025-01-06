from django.contrib import admin
from .models import MstComponent, MstCategory, MstSubCategory, MstSectionRules, MstDesignOptions, MstSubCategoryRelations, MstSubCategoryTwo
# Register your models here.
admin.site.register(MstComponent)
admin.site.register(MstCategory)
admin.site.register(MstSubCategory)
admin.site.register(MstSectionRules)
admin.site.register(MstDesignOptions)
admin.site.register(MstSubCategoryRelations)
admin.site.register(MstSubCategoryTwo)
