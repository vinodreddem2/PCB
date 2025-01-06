from django.http import Http404
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import get_categories_for_component_id
from authentication.custom_permissions import IsAuthorized
from authentication.custom_authentication import CustomJWTAuthentication


class ComponentDetailedAPIView(APIView):
    permission_classes = [IsAuthorized]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request, component_id):
        
        try:            
            response = get_categories_for_component_id(component_id)            
            return Response(response["data"], status=status.HTTP_200_OK) 
        
        except Http404 as e:            
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error": "Exception Occurred {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Use Functions inside services
# Fetch All Section Groupings for given sub_catogory id
# Fetch Rules for each grouping 

# Add Persmission class
class SectionGroupings(APIView):
    def get(self, request, sub_category_id):
        pass


# Fetch SUb 2 Cateogies for selected sub category
# Add Persmission class
class SubTwoCategory(APIView):
    def get(self, request, sub_category_id):
        pass


# Add Persmission class
# This is used to store the form data submitted from the front end
# COnvert the data into JSON format as per the selections on front end
class CADDesignTemplate(APIView):
    def post(self, request):
        pass
