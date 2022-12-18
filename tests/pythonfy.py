""""

        Converting Hope lang type into python types 


"""

from Hope import * 
def convert_from_hope_to_python_objects(object):
    if not isinstance(object,List): return object.value
    result = []

    for element in object.elements:
        result.append(convert_from_hope_to_python_objects(element))
    
    return result
    
    