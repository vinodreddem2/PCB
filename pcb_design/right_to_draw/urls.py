from django.urls import path

from .views import (ComponentDetailedAPIView,SectionGroupingsAPIView,
                    SubCategoryTwoAPIView,CADDesignTemplatesAPIView,
                    RequestPasswordResetView,PasswordResetView
                    )

urlpatterns = [
    path('pcb-specification/<int:component_id>/', ComponentDetailedAPIView.as_view()),
    path("section-groupings/<int:sub_category_id>/", SectionGroupingsAPIView.as_view(), name="section-groupings"),
    path('sub-categories-two/<int:sub_category_id>/', SubCategoryTwoAPIView.as_view(), name='sub-categories-two'),
    path('cad_design-templates/', CADDesignTemplatesAPIView.as_view(), name='design-templates'),
    path('request-reset-password/', RequestPasswordResetView.as_view(), name='request-reset-password'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
]