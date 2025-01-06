from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import ComponentHierarchyService
from authentication.custom_permissions import IsAuthorized
from authentication.custom_authentication import CustomJWTAuthentication
class ComponentDetailedAPIView(APIView):
    permission_classes = [IsAuthorized]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request, component_id):
        
        try:
            
            response = ComponentHierarchyService.get_hierarchy_by_component_id(component_id)
            
            return Response(response["data"], status=status.HTTP_200_OK) 
            
        except Exception as e:
            return Response(
                {
                    "error": "Failed to retrieve component",
                    "detail": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
