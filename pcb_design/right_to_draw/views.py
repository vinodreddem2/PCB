from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from authentication.custom_permissions import IsAuthorized
from authentication.custom_authentication import CustomJWTAuthentication
from .models import CADDesignTemplates
from .services import get_categories_for_component_id, create_cad_template,\
    get_sub_categories_two_for_subcategory_id,  get_design_options_for_sub_category,get_design_rules_for_design_option,\
    get_verifier_fields_by_params, create_cad_verifier_template, compare_verifier_data_with_rules_and_designs, get_verifier_record
from drf_yasg.utils import swagger_auto_schema
from .serializers import CADDesignTemplatesSerializer
from . import right_to_draw_logs


class ComponentAPIView(APIView):
    permission_classes = [IsAuthorized]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request, component_id):
        is_verifier = int(request.GET.get('is_verifier', 0))
        try:
            right_to_draw_logs.info(f"Get Component API View called for: {component_id}, is_verfier:'{is_verifier}' -- user:{request.user}")            
            response = get_categories_for_component_id(component_id, is_verifier)
            l_response = len(response)
            right_to_draw_logs.info(f"Get Component Data for: {component_id}, is_verfier:{is_verifier} --- No: Categories:{l_response}")
            return Response(response, status=status.HTTP_200_OK) 
        
        except Http404 as e:
            right_to_draw_logs.info(f"Http404 Error in Component API View for component_id: {component_id} -- user: {request.user} -- {str(e)}")
            right_to_draw_logs.error(f"Http404 Error in Component API View for component_id: {component_id} -- user: {request.user} -- {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            error_log = f"Exception Occurred in Component API View for component_id: {component_id} -- user: {request.user} -- {str(e)}"
            right_to_draw_logs.info(error_log)
            right_to_draw_logs.error(error_log)
            return Response({"error": f"Exception Occurred {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


class DesignOptionAPIView(APIView):
    permission_classes = [IsAuthorized]
    authentication_classes = [CustomJWTAuthentication]
    def get(self, request, sub_category_id):
        try:
            response =  get_design_options_for_sub_category(sub_category_id)
            return Response(response, status=status.HTTP_200_OK)
        except Http404 as e:            
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DesignRuleAPIView(APIView):
    permission_classes = [IsAuthorized]
    authentication_classes = [CustomJWTAuthentication]
    def get(self, request):        
        try:
            design_option_ids = request.query_params.get('design_option_ids', None)            
            if design_option_ids:
                design_option_ids = design_option_ids.split(',')                
                design_option_ids = [int(id.strip()) for id in design_option_ids]
                response =  get_design_rules_for_design_option(design_option_ids)
                return Response(response, status=status.HTTP_200_OK)
            else:
                raise Http404("No design_option_ids provided")
        except Http404 as e:            
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CADDesignTemplatesAPIView(APIView):
    permission_classes = [IsAuthorized]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request, *args, **kwargs):        
        cad_template_id = request.query_params.get('id', None)

        if cad_template_id:
            try:                
                cad_template = CADDesignTemplates.objects.get(id=cad_template_id)                
                serializer = CADDesignTemplatesSerializer(cad_template)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except CADDesignTemplates.DoesNotExist:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        else:            
            cad_templates = CADDesignTemplates.objects.all()            
            serializer = CADDesignTemplatesSerializer(cad_templates, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'oppNumber': openapi.Schema(type=openapi.TYPE_STRING, description='Opportunity Number'),
                'opuNumber': openapi.Schema(type=openapi.TYPE_STRING, description='Opu Number'),
                'eduNumber': openapi.Schema(type=openapi.TYPE_STRING, description='Education Number'),
                'modelName': openapi.Schema(type=openapi.TYPE_STRING, description='Model Name'),
                'partNumber': openapi.Schema(type=openapi.TYPE_STRING, description='Part Number'),
                'revisionNumber': openapi.Schema(type=openapi.TYPE_STRING, description='Revision Number'),
                'component': openapi.Schema(type=openapi.TYPE_INTEGER, description='Component ID (e.g., b14)'),
                'componentSpecifications': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    additional_properties=openapi.Schema(type=openapi.TYPE_STRING, description="Dynamic specification fields")
                ),
                'designOptions': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING),
                    description='Design options (array of strings)'
                )
            },
            required=['oppNumber', 'opuNumber', 'modelName', 'partNumber', 'component'],
        ),
        responses={201: 'Template Created', 400: 'Bad Request'}
    )
    def post(self, request):
        user = request.user
        template, error = create_cad_template(request.data, user)        
        if error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(template.id, status=status.HTTP_201_CREATED)


class MstVerifierFieldFilterAPIView(APIView):
    permission_classes = [IsAuthorized]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):        
        component_id = request.query_params.get('component_id', None)
        category_id = request.query_params.get('category_id', None)
        sub_category_id = request.query_params.get('sub_category_id', None)

        try:            
            serialized_data = get_verifier_fields_by_params(
                component_id=component_id,
                category_id=category_id,
                sub_category_id=sub_category_id
            )                        

            return Response(serialized_data, status=status.HTTP_200_OK)

        except Exception as e:            
            return Response({"error": f"Exception occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CADVerifierTemplateCreateAPIView(APIView):
    permission_classes = [IsAuthorized]
    authentication_classes = [CustomJWTAuthentication]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'oppNumber': openapi.Schema(type=openapi.TYPE_STRING, description='Opp Number'),
                'opuNumber': openapi.Schema(type=openapi.TYPE_STRING, description='Opu Number'),
                'eduNumber': openapi.Schema(type=openapi.TYPE_STRING, description='Edu Number'),
                'modelName': openapi.Schema(type=openapi.TYPE_STRING, description='Model Name'),
                'partNumber': openapi.Schema(type=openapi.TYPE_STRING, description='Part Number'),
                'revisionNumber': openapi.Schema(type=openapi.TYPE_STRING, description='Revision Number'),
                'component': openapi.Schema(type=openapi.TYPE_INTEGER, description='Component ID (e.g., b14)'),
                'componentSpecifications': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    additional_properties=openapi.Schema(type=openapi.TYPE_STRING, description="Dynamic specification fields")
                ),
                'verifierQueryData': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    additional_properties=openapi.Schema(type=openapi.TYPE_STRING, description="Verifier query fields")
                )
            },
            required=['oppNumber', 'opuNumber', 'modelName', 'partNumber', 'component'],
        ),
        responses={201: 'Template Created', 400: 'Bad Request'}
    )
    def post(self, request):
        try:
            user = request.user
            try:
                template, error = create_cad_verifier_template(request.data, user)
            except Exception as e:
                print("Excetion Occuring on storing the record")
            res = compare_verifier_data_with_rules_and_designs(request.data)
            if error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
                    
            return Response({"template_id":template.id, "res":res}, status=status.HTTP_201_CREATED)
        except Exception as e:            
            return Response({"error": f"Exception occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class MstVerifierFieldResultAPIView(APIView):
    permission_classes = [IsAuthorized]
    authentication_classes = [CustomJWTAuthentication]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'oppNumber': openapi.Schema(type=openapi.TYPE_STRING, description='Opp Number'),
                'opuNumber': openapi.Schema(type=openapi.TYPE_STRING, description='Opu Number'),
                'eduNumber': openapi.Schema(type=openapi.TYPE_STRING, description='Edu Number'),
                'modelName': openapi.Schema(type=openapi.TYPE_STRING, description='Model Name'),
                'partNumber': openapi.Schema(type=openapi.TYPE_STRING, description='Part Number'),
                'revisionNumber': openapi.Schema(type=openapi.TYPE_STRING, description='Revision Number'),
                'component': openapi.Schema(type=openapi.TYPE_INTEGER, description='Component ID (e.g., b14)')                
            },
            required=['oppNumber', 'opuNumber', 'modelName', 'partNumber', 'component'],
        ),
        responses={201: 'Results Created', 400: 'Bad Request'}
    )
    def post(self, request):
        try:            

            verifier_record_data = get_verifier_record(request.data)     
            res = compare_verifier_data_with_rules_and_designs(verifier_record_data)
            return Response({"res":res}, status=200)

        except Exception as e:            
            return Response({"error": f"Exception occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
