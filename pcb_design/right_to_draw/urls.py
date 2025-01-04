from django.urls import path
from .views import ComponentCategoryAPIView

urlpatterns = [
    path('pcb_specification/<int:component_id>/', ComponentCategoryAPIView.as_view()),
]