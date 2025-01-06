from masters.models import MstComponent
from .serializers import CustomComponentSerializer
class ComponentHierarchyService:
    @staticmethod
    def get_hierarchy_by_component_id(component_id):
        """
        Fetch the component hierarchy based on the given component_id.

        :param component_id: UUID of the component.
        :return: Serialized component hierarchy data or an error message.
        """
        try:
            # Fetch the component by id
            component = MstComponent.objects.prefetch_related(
                "component_categories__subcategories__subcategory"
            ).get(id=component_id)

            # Serialize the component hierarchy
            serialized_data = CustomComponentSerializer.from_model(component)
            return {"success": True, "data": serialized_data}

        except MstComponent.DoesNotExist:
            return {"success": False, "error": f"Component with id {component_id} does not exist."}

        except Exception as e:
            return {"success": False, "error": str(e)}
