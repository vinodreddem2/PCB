from django.http import Http404

from masters.models import MstComponent
from masters.models import MstSectionGroupings, MstSubCategoryTwo


def get_categories_for_component_id(component_id):
    try:
        component = MstComponent.objects.prefetch_related(
            'component_categories',
            'component_categories__subcategories'
        ).get(id=component_id)

        categories = component.component_categories.all()

        result = []
        
        for category in categories:            
            subcategories = category.subcategories.all()
            subcategory_data = [
                {
                    'id': subcategory.id,
                    'name': subcategory.name,
                    'is_section_groupings_exists': MstSectionGroupings.objects.filter(subcategory=subcategory).exists(),
                    'is_sub_2_categories_exists': MstSubCategoryTwo.objects.filter(subcategory=subcategory).exists()
                }
                for subcategory in subcategories
            ]
            result.append({
                'category_id': category.id,
                'category_name': category.name,
                'subcategories': subcategory_data
            })

        return result
        
    except MstComponent.DoesNotExist:

        raise Http404("Component with the given ID does not exist.")
