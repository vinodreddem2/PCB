from django.http import Http404
from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import CADVerifierTemplates, CADDesignTemplates
from masters.models import MstComponent, MstSubCategoryTwo, MstDesignOptions, MstSectionRules, \
    MstSectionGroupings, MstVerifierField, MstVerifierField, MstVerifierRules, MstCategory, MstSubCategory
from .serializers import SectionGroupingsSerializer,SubCategoryTwoSerializer, CADDesignTemplatesSerializer, \
    SectionRulesSerializer, MstVerifierFieldSerializer, CADVerifierTemplateSerializer
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist


def get_categories_for_component_id(component_id, is_verifier=0):
    try:
        component = MstComponent.objects.prefetch_related(
            'component_categories',
            'component_categories__subcategories'
        ).get(id=component_id)

        if is_verifier == 1:
            categories = component.component_categories.filter(is_verifier=True)
        else:
            categories = component.component_categories.all()

        result = []
        
        for category in categories:            
            if is_verifier == 1:
                subcategories = category.subcategories.filter(is_verifier=True)
            else:
                subcategories = category.subcategories.all()
                
            subcategory_data = [
                {
                    'id': subcategory.id,
                    'name': subcategory.sub_category_name,
                    'is_design_options_exists': MstDesignOptions.objects.filter(sub_category_id=subcategory).exists(),
                    'is_sub_2_categories_exists': MstSubCategoryTwo.objects.filter(sub_category_id=subcategory).exists(),
                    'has_verifier_fields': MstVerifierField.objects.filter(sub_category=subcategory).exists()
                }
                for subcategory in subcategories
            ]
            
            result.append({
                'category_id': category.id,
                'category_name': category.category_name,
                'subcategories': subcategory_data
            })
    

        return result
        
    except MstComponent.DoesNotExist:

        raise Http404("Component with the given ID does not exist.")


def get_sub_categories_two_for_subcategory_id(sub_category_id):
    try:        
        sub_categories_two = MstSubCategoryTwo.objects.filter(sub_category_id=sub_category_id)
        
        if not sub_categories_two:
            return Response({"message": "No sub-categories two found for the given subcategory."}, status=404)
         
        serialized_data = SubCategoryTwoSerializer(sub_categories_two, many=True)
        
        return serialized_data
    except MstSubCategoryTwo.DoesNotExist:
        
        raise Http404("Sub-2 Categories with the given ID does not exist.")
    

def get_design_options_for_sub_category(sub_category_id):
    try:     
        design_options = MstDesignOptions.objects.filter(sub_category_id=sub_category_id)
        
        if not design_options.exists():
            raise Http404("No Design Options found for the given Sub Category ID.")
        
        result = []
        for design_option in design_options:
            result.append({
                'design_option_id': design_option.id,
                'desing_option_name': design_option.desing_option_name
            })
        
        print("vinod result is ", result)
        return result

    except Exception as e:
        raise Http404(f"An error occurred while fetching design options: {str(e)}")


def get_design_rules_for_design_option(design_option_ids):
    
    try:
        design_options = MstDesignOptions.objects.prefetch_related('section_groups__rules').filter(id__in=design_option_ids)
        
        rules_data = []
        unique_rule_ids = set()

        for design_option in design_options:            
            for group in design_option.section_groups.all():                
                for rule in group.rules.all():
                    if rule.id not in unique_rule_ids:
                        unique_rule_ids.add(rule.id)
                        rule_serializer = SectionRulesSerializer(rule)
                        rules_data.append(rule_serializer.data)

        return rules_data

    except Exception as e:
        raise Http404(f"An error occurred while fetching design rules: {str(e)}")
    
 
def create_cad_template(data, user):
    component_id = data.get('component')
    component_specifications = data.get('componentSpecifications')
    design_options = data.get('designOptions')
    
    try:
        component = MstComponent.objects.get(id=component_id)
    except MstComponent.DoesNotExist:
        return None, {"error": "Component not found."}

    data_for_serializer = {
        "opp_number": data.get("oppNumber"),
        "opu_number": data.get("opuNumber"),
        "edu_number": data.get("eduNumber"),
        "model_name": data.get("modelName"),
        "part_number": data.get("partNumber"),
        "revision_number": data.get("revisionNumber"),
        "component_Id": component.pk,
        "pcb_specifications": component_specifications,
        "smt_design_options": design_options,
        'created_by':user.pk,
        'updated_by': user.pk
    }

    # Create and validate the serializer
    serializer = CADDesignTemplatesSerializer(data=data_for_serializer)
    if serializer.is_valid():        
        cad_template = serializer.save()
        return cad_template, None
    else:        
        return None, serializer.errors


def get_verifier_fields_by_params(component_id=None, category_id=None, sub_category_id=None):    
    filter_criteria = Q()
    if component_id:
        filter_criteria &= Q(component_id=component_id)
    if category_id:
        filter_criteria &= Q(category_id=category_id)
    if sub_category_id:
        filter_criteria &= Q(sub_category__id=sub_category_id)
    verifier_fields = MstVerifierField.objects.filter(filter_criteria).distinct().order_by('id')

    serializer = MstVerifierFieldSerializer(verifier_fields, many=True)

    return serializer.data


def create_cad_verifier_template(data, user):
    component_id = data.get('component')
    design_compare_data = data.get('design_compare_data', [])
    verify_compare_data = data.get('verify_compare_data', [])    
    try:
        component = MstComponent.objects.get(id=component_id)
    except MstComponent.DoesNotExist:
        return None, {"error": "Component not found."}
    
    template_data = {
        "opp_number": data.get("oppNumber"),
        "opu_number": data.get("opuNumber"),
        "edu_number": data.get("eduNumber"),
        "model_name": data.get("modelName"),
        "part_number": data.get("partNumber"),
        "revision_number": data.get("revisionNumber"),
        "component_Id": component.pk,
        "pcb_specifications": data.get("componentSpecifications", {}),
        "verifier_query_data": data.get("verifierQueryData", {}),
        'created_by':user.pk,
        'updated_by': user.pk
    }

    # Create and validate the serializer
    serializer = CADVerifierTemplateSerializer(data=template_data)
    if serializer.is_valid():
        cad_verifier_template = serializer.save()            
        return cad_verifier_template, None
    else:
        return None, serializer.errors


def compare_verifier_data_with_design_data(data):    
    design_specifications_data = data.get('componentSpecifications')
    opp_number = data.get("oppNumber")
    opu_number = data.get("opuNumber")
    edu_number = data.get("eduNumber")
    model_name = data.get("modelName")
    part_number = data.get("partNumber")
    revision_number = data.get("revisionNumber")
    component_id = data.get('component')
    design_specifications_data = data.get('componentSpecifications')

    design_verification_res = []

    template = CADDesignTemplates.objects.filter(
        opp_number=opp_number,
        opu_number=opu_number,
        edu_number=edu_number,
        model_name=model_name,
        part_number=part_number,
        revision_number=revision_number,
        component_Id=component_id
    ).first()

    if not template:
        raise ValueError("No matching CADDesignTemplate found.")
    pcb_specifications_str = template.pcb_specifications 

    print("vinod type of the pcb_specifications", pcb_specifications_str)
    print(type(pcb_specifications_str))

    pcb_specifications = {int(k):int(v) for k, v in pcb_specifications_str.items()}
    # import pdb
    # pdb.set_trace()
    for category_id, selected_sub_category_id in design_specifications_data.items():
        # pdb.set_trace()
        category_id = int(category_id)
        selected_sub_category_id = int(selected_sub_category_id)
        try:
            category = MstCategory.objects.get(id=category_id)
        except ObjectDoesNotExist as ex:
            is_deviated = False
            deviation_result = {
                'categor_id' : category_id,
                'name': "Invalid Category Id",
                'selected_deviation_id': "N/A",
                'selected_deviation_name': "N/A",
                'is_deviated': True
            }
            design_verification_res.append(deviation_result)
            continue
        
        # For Dielectric Thickness, The Verifer enter the value manually Instead of selecting from Drop Down
        if category.category_name.strip() == 'Dielectric Thickness':
            selected_val = float(selected_sub_category_id)
            if category_id in pcb_specifications:
                dielectric_thickness_sub_category = pcb_specifications.get(category_id)
                sub_category = MstSubCategory.objects.get(id=selected_sub_category_id)
                val = float(sub_category.name.strip('"'))
                if val != selected_val:
                    is_deviated = True

                deviation_result = {
                    'categor_id' : category_id,
                    'name': category.category_name,
                    'selected_deviation_id': "N/A",
                    'selected_deviation_name': selected_val,
                    'is_deviated': is_deviated
                }
                design_verification_res.append(deviation_result)
                continue
                

        else:
            try:
                sub_category = MstSubCategory.objects.get(id=selected_sub_category_id)
            except ObjectDoesNotExist:                
                deviation_result = {
                    'categor_id' : category_id,
                    'name': category.category_name,
                    'selected_deviation_id': selected_sub_category_id,
                    'selected_deviation_name': "N/A",
                    'is_deviated': False
                }
                design_verification_res.append(deviation_result)
                continue                
            if category_id in pcb_specifications:            
                if pcb_specifications.get(category_id) != selected_sub_category_id:                
                    is_deviated = True                
                else:
                    is_deviated = False                    
            else:
                is_deviated = False
            
            deviation_result = {
                'categor_id' : category_id,
                'name': category.category_name,
                'selected_deviation_id': selected_sub_category_id,
                'selected_deviation_name': sub_category.sub_category_name,
                'is_deviated': is_deviated 
            }

            design_verification_res.append(deviation_result)
    
    return design_verification_res


def comapre_verfier_data_with_rules(verifier_id, field_value):    
    try:
        verifier_field = MstVerifierField.objects.get(id=int(verifier_id))        
        verifier_rule = MstVerifierRules.objects.get(verifier_field=verifier_field.pk)        
        rule_number = verifier_rule.rule_number
        design_doc = verifier_rule.design_doc                
        section_rule = MstSectionRules.objects.get(rule_number=rule_number, design_doc=design_doc)
        try:        
            min_value = float(section_rule.min_value) if section_rule.min_value else None                   
        except Exception as e:
            min_value = None

        try:                    
            max_value = float(section_rule.max_value) if section_rule.max_value else None        
        except Exception as e:
            max_value = None


        is_deviation = False
        if (min_value is not None and field_value < min_value) or (max_value is not None and field_value > max_value):
            is_deviation = True
        
        return is_deviation

    except ObjectDoesNotExist as ex:
        return False
    except Exception as ex:
        return False

def comapre_verfier_data(verified_data):
    verifier_res = []
    for id, val in verified_data.items():
        val = float(val)
        is_deviated = comapre_verfier_data_with_rules(id, val)
        verifier_field = MstVerifierField.objects.get(id=id)
        name = verifier_field.name
        data = {'id' :id, 'name':name, 'value':val, 'is_deviated':is_deviated}
        verifier_res.append(data)
    return verifier_res


def compare_verifier_data_with_rules_and_designs(data):    
    res = {
        "opp_number": data.get("oppNumber"),
        "opu_number": data.get("opuNumber"),
        "edu_number": data.get("eduNumber"),
        "model_name": data.get("modelName"),
        "part_number": data.get("partNumber"),
        "revision_number": data.get("revisionNumber"),        
    }
    # import pdb
    # pdb.set_trace()  
    verified_rule_data = comapre_verfier_data(data.get("verifierQueryData"))
    res['verified_query_data'] = verified_rule_data

    design_specification_data = compare_verifier_data_with_design_data(data)
    res['verify_design_fields_data']= design_specification_data
    return res



def get_verifier_record(request_data):
    """
    This function takes the request data, queries the CADVerifierTemplates table
    based on the parameters provided, and returns the data in the required format.
    """

    # Extract the parameters from the request data
    opp_number = request_data.get('oppNumber')
    opu_number = request_data.get('opuNumber')
    edu_number = request_data.get('eduNumber')
    model_name = request_data.get('modelName')
    part_number = request_data.get('partNumber')
    revision_number = request_data.get('revisionNumber')
    component_id = request_data.get('component')

    # Query the CADVerifierTemplates table based on the parameters
    try:
        verifier_record = CADVerifierTemplates.objects.get(
            opp_number=opp_number,
            opu_number=opu_number,
            edu_number=edu_number,
            model_name=model_name,
            part_number=part_number,
            revision_number=revision_number,
            component_Id=component_id
        )
    except ObjectDoesNotExist as ex:
        raise ObjectDoesNotExist('Verifier record not found.')

    # Prepare the response data in the required format
    response_data = {
        'oppNumber': verifier_record.opp_number,
        'opuNumber': verifier_record.opu_number,
        'eduNumber': verifier_record.edu_number,
        'modelName': verifier_record.model_name,
        'partNumber': verifier_record.part_number,
        'revisionNumber': verifier_record.revision_number,
        'component': verifier_record.component_Id.id,

        'componentSpecifications': verifier_record.pcb_specifications,
        'verifierQueryData': verifier_record.verifier_query_data
    }

    return response_data