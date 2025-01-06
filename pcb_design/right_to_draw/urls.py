from django.urls import path
from .views import ComponentDetailedAPIView

urlpatterns = [
    path('pcb_specification/<int:component_id>/', ComponentDetailedAPIView.as_view()),
]