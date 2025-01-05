from rest_framework.views import APIView
from rest_framework.response import Response
from masters.models import MstCategory
from .serializers import CategorySerializer

class ComponentCategoryAPIView(APIView):
    def get(self, request, component_id, format=None):
        categories = MstCategory.objects.filter(component_id=component_id)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    # [{id:,category_name:,sub_category:[{id:,name:}]}]
    
    # Services.py ---> Create a fn based on requirement 
    # MSTCategory ----> Each Cat get SubCategories (id,name) ---> [{id:,name:,sub_category:[{id:,name:}]}]