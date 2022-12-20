""""

        Converting Hope lang type into python types 


"""

from Hope import * 


def make_tokens(string: str):
    strings = string.split(":")
    print(strings)
    
def remove_quotes(string: str):
    return string[1:-1]

def convert_from_hope_to_python_objects(object):
    if hasattr(object,'value'):
        if isinstance(object,String):
            if "'" in object.value or '"' in object.value:
                return remove_quotes(object.value)
            else:
                return object.value

        if '.' in str(object.value): 
            return float(object.value)

        return int(object.value)
    
    if isinstance(object,(List,list)) or hasattr(object,'elements'):
        result = []
        elements = object.elements  if hasattr(object,'elements') else object

        for element in elements:
            result.append(convert_from_hope_to_python_objects(element))
        
        if type(object) == list and len(result) == 1:
                return result[0]

        return result
    
    return object

def matches(result,Expected_result):
    result = convert_from_hope_to_python_objects(result)
    if result is None:
        if Expected_result is None:
            return True
        return False


    if len(result) != len(Expected_result) : return False

    for idx,expected_result_element in enumerate(Expected_result):
        result_element = result[idx]

        if type(expected_result_element) == type:
            if not isinstance(result_element,expected_result_element):
                return False
                
        elif expected_result_element != result_element:
            return False
    
    return True

