__all__ = ['check_not_none',
           'check_true_to_append',
           'check_true_to_set',
           'get_json_key_value'
          ]

def get_json_key_value(dic, key):
    if dic:
        hit   = []
        stack = list(zip(dic.keys(), dic.values()))
        while stack :
            k,v = stack.pop()
            if k == key:
                hit.append(v)
            if isinstance(v, dict):
                stack.extend(list(zip(v.keys(), v.values()))) 

        if len(hit) == 1: return hit[0]
        if len(hit) > 1 : return "multiple_key"
    else: return None


def check_not_none(value):
    status = False
    if value and value != "None": 
        status = True 
    return status
        
    
def check_true_to_append(dic, key, items_list):
    value = get_json_key_value(dic, key)
    if check_not_none(value): items_list.append(value)
    return items_list


def check_true_to_set(dic1, key1, dic2, key2):
    value = get_json_key_value(dic1, key1)
    if check_not_none(value): dic2[key2] = value
    return dic2