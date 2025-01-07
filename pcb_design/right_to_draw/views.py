from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from authentication.custom_permissions import IsAuthorized
from authentication.custom_authentication import CustomJWTAuthentication
from .models import CADDesignTemplates
from .services import get_categories_for_component_id,get_section_groupings_for_subcategory_id, \
    get_sub_categories_two_for_subcategory_id, create_cad_template


class ComponentDetailedAPIView(APIView):
    permission_classes = [IsAuthorized]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request, component_id):
        print(component_id)
        
        try:            
            response = get_categories_for_component_id(component_id)            
            return Response(response, status=status.HTTP_200_OK) 
        
        except Http404 as e:            
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error": f"Exception Occurred {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SectionGroupingsAPIView(APIView):
    permission_classes = [IsAuthorized]
    authentication_classes = [CustomJWTAuthentication]
    def get(self, request, sub_category_id):
        try:
            response = get_section_groupings_for_subcategory_id(sub_category_id)
            return Response(response.data, status=status.HTTP_200_OK)
        except Http404 as e:            
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubCategoryTwoAPIView(APIView):
    permission_classes = [IsAuthorized]
    authentication_classes = [CustomJWTAuthentication]
    def get(self, request, sub_category_id):
        try:
            response =  get_sub_categories_two_for_subcategory_id(sub_category_id)
            return Response(response.data, status=status.HTTP_200_OK)
        except Http404 as e:            
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CADDesignTemplatesAPIView(APIView):
    permission_classes = [IsAuthorized]
    authentication_classes = [CustomJWTAuthentication]
    
    def post(self, request):        
        template, error = create_cad_template(request.data)        
        if error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(template.id, status=status.HTTP_201_CREATED)
