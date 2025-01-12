from django.urls import path

from .views import ComponentDetailedAPIView, SubCategoryTwoAPIView,\
    CADDesignTemplatesAPIView, DesignOptionAPIView,DesignRuleAPIView

urlpatterns = [
    path('pcb-specification/<int:component_id>/', ComponentDetailedAPIView.as_view()),    
    path('sub-categories-two/<int:sub_category_id>/', SubCategoryTwoAPIView.as_view(), name='sub-categories-two'),
    path('cad-design-templates/<int:id>/', CADDesignTemplatesAPIView.as_view(), name='design-templates'),
    path('cad-design-templates/', CADDesignTemplatesAPIView.as_view(), name='design-templates'),
    path('design-options/<int:sub_category_id>/', DesignOptionAPIView.as_view(), name='design-options'),
    path('design-rules/<int:design_option_id>/', DesignRuleAPIView.as_view(), name='design-rules'),
]